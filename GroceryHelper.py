#Make basic flask application with root page that return "Hello World"
from flask import Flask, request, render_template, redirect
from webscraping import scrapeAmazon
from webscraping import scrapeAuchan
from webscraping import scrapeAuchanProduct
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import copy

# Inicializando a aplicação Flask
app = Flask(__name__)

# Carregar a key da API que está no .env
load_dotenv('.env')

# Definir a rota da página inicial
@app.route('/')
def home():
    return render_template('home.html')

# Definir a rota /products que aceita requisições POST
@app.route('/products', methods=['POST'])
def products():
    """
    Esta função é responsável por receber um texto do formulário de requisição, extrair os produtos alimentícios e bebidas desse texto usando a API da OpenAI, fazer scraping dos detalhes desses produtos do site Auchan e renderizar um template HTML com esses produtos.

    1. O texto é obtido do formulário de requisição.
    2. Se o arquivo 'output.json' existir, ele é removido.
    3. A função tenta inicializar o cliente OpenAI com a chave da API armazenada em um arquivo '.env'.
    4. A função cria uma tarefa de conclusão com a API da OpenAI, passando uma mensagem de sistema que define o papel do modelo e uma mensagem de usuário que contém o texto recebido.
    5. A função extrai a saída da tarefa de conclusão, que é uma lista de produtos em formato JSON.
    6. A função faz scraping dos detalhes de cada produto do site Auchan e armazena-os em um dicionário.
    7. A função modifica o link de cada produto para incluir o domínio completo do site Auchan.
    8. A função renderiza o template 'products.html', passando o dicionário de produtos como um argumento.

    :return: Um template renderizado com os produtos extraídos.
    """
    text = request.form.get('product')
    print("== Texto recebido ==============================")
    print(text)
    print("================================================")
    
    if os.path.exists("output.json"):
        os.remove("output.json")
    
    try: 
        client = OpenAI(
            api_key = os.environ.get('OPENAI_API_KEY')
        )
    except:
        return "A key da API da OpenAI deve estar guardada num ficheiro chamado '.env', no seguinte formado: OPENAI_API_KEY=<key>"
    
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a product selection assistant who has received a text. Your job is to take this text and extract all the food products, including beverages. Your output should be these food products and beverages in an array in JSON format called Products." },
            {"role": "user", "content": f"Text:\n{text}"}
        ]
    )
    
    output = completion.choices[0].message.content
    output = json.loads(output)['Products']
    print("== Produtos extraídos do texto recebido ========")
    print(output)
    print("================================================")

    products = {}
    for product in output:
        products[product] = scrapeAuchan(product)
    
    for product, details in products.items():
        for item in details:
            # tirar a primeira / do link
            item['link'] = "https://www.auchan." + item['link'][1:]

    
    print("== Return do scraping =========================")
    print(products)
    print("================================================")

    return render_template('products.html', products=products)

# Definir a rota /productsSelection que aceita requisições POST
@app.route('/productsSelection', methods=['POST'])
def productsSelection():
    """
    Processa as informações dos produtos selecionados a partir de uma requisição POST.

    A função obtém a lista de produtos selecionados a partir do formulário da requisição POST.
    Em seguida, para cada produto, ela verifica se o produto contém informações adicionais ('infos').
    Se contiver, ela extrai o nome, preço, link e informações do produto e adiciona ao dicionário de produtos selecionados.
    Se não contiver, ela extrai apenas o nome, preço e link do produto.
    Depois, para cada produto selecionado, se o produto não contiver detalhes, ela realiza o scraping dos detalhes do produto a partir do link do produto.
    Finalmente, ela imprime os produtos selecionados e renderiza o template 'questions.html' com os produtos selecionados.

    Returns:
        render_template: Renderiza o template 'questions.html' com os produtos selecionados.
    """
    selected_products_info = request.form.getlist('selected_products')
    selected_products = []

    for product_info in selected_products_info:
        if "infos" in product_info:
            parts = product_info.split(',')
            name = parts[0].strip()
            price = parts[1].strip()
            link = parts[2].strip()
            infos = ','.join(parts[3:]).strip()
            
            selected_products.append({
                'name': name,
                'price': price,
                'link': link,
                'infos': infos,
            })
        else: 
            name, price, link = product_info.split(',')
            selected_products.append({
                'name': name,
                'price': price,
                'link': link,
            })

    for product in selected_products:
        if 'details' not in product:
            product['details'] = scrapeAuchanProduct(product['link'])

    print("== Produtos selecionados =======================")
    for product in selected_products:
        print(f"Nome: {product['name']}, Preço: {product['price']}, Link: {product['link']}, Detalhes: {product['details']}")
    print("================================================")

    return render_template('questions.html', selected_products=selected_products)

# Definir a rota /submitQuestion que aceita requisições POST
@app.route('/submitQuestion', methods=['POST'])
def submitQuestion():
    """
    Esta função é responsável por receber uma lista de produtos selecionados do formulário de requisição, extrair as informações desses produtos, fazer scraping dos detalhes de cada produto do site Auchan (se necessário) e renderizar um template HTML com esses produtos.

    1. A função obtém a lista de produtos selecionados do formulário de requisição.
    2. Para cada produto na lista, a função extrai o nome, preço e link do produto. Se o produto contém informações adicionais, elas também são extraídas.
    3. A função adiciona cada produto a uma nova lista de produtos selecionados.
    4. Para cada produto na nova lista, se o produto não contém detalhes, a função faz scraping dos detalhes do produto do site Auchan.
    5. A função imprime os detalhes de cada produto na lista de produtos selecionados.
    6. A função renderiza o template 'questions.html', passando a lista de produtos selecionados como um argumento.

    :return: Um template renderizado com os produtos selecionados.
    """
    question = request.form.get('question')
    selected_products = request.form.getlist('selected_products')
    print("== Pergunta recebida =========================")
    print("Pergunta recebida:", question)
    print("Produtos selecionados:", selected_products)
    print("==============================================")
    
    try:
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        answer = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            response_format={"type": "text"},
            messages=[
                {"role": "system", "content": f"You are assisting a customer who has selected several products. Please provide answers to their questions based on the following products and any additional context provided. The selected products are: {selected_products}"},
                {"role": "user", "content": f"Question: {question}"}
                ]
            )
        print("================================================")
        print("Resposta gerada pelo ChatGPT: ")
        print(answer)
        print("================================================")
        answer = answer.choices[0].message.content
    except Exception as e:
        answer = f"Ocorreu um erro ao processar a pergunta: {str(e)}"
    
    print("== Resposta gerada pelo ChatGPT =================")
    print(answer)
    print("================================================")
    
    return render_template('answer.html', question=question, answer=answer, selected_products=selected_products)