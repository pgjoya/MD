from scrapy.crawler import CrawlerProcess
from myspider.myspider.spiders.amazon import AmazonSpider
from myspider.myspider.spiders.auchan import AuchanSpider
from myspider.myspider.spiders.auchanProduct import AuchanProductSpider
import json
import os
from multiprocessing import Process

def scrapeAmazon(productName):
    """
    Esta função é responsável por fazer scraping dos detalhes de um produto específico do site da Amazon.

    1. A função inicializa um processo de rastreamento com um agente de usuário específico e configurações de saída.
    2. A função inicia um rastreamento do Spider da Amazon com o nome do produto como argumento.
    3. A função inicia o processo de rastreamento.
    4. A função abre o arquivo 'output.json', carrega os dados em formato JSON e imprime os dados.
    5. A função trunca o arquivo 'output.json' para remover os dados antigos.
    6. A função filtra os dados para remover quaisquer itens que contenham valores None.
    7. A função retorna os dados filtrados.

    :param productName: O nome do produto para fazer scraping.
    :return: Uma lista de dicionários contendo os detalhes do produto.
    """
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    })

    data = process.crawl(AmazonSpider, product=productName)
    process.start()
    
    print("================================================")
    print("O spider deu:\n")
    
    with open('output.json', 'r') as file:
        data = json.load(file)
        print(data)
    print("================================================")
        

    with open('output.json', 'w') as file:
        file.truncate(0)

    data = [item for item in data if None not in item.values()]
    
    return data

def scrapeAuchanProcess(productName):
    """
    Esta função é responsável por iniciar um processo de rastreamento para fazer scraping dos detalhes de um produto específico do site da Auchan.

    1. A função inicializa um processo de rastreamento com um agente de usuário específico e configurações de saída.
    2. A função inicia um rastreamento do Spider da Auchan com o nome do produto como argumento.
    3. A função inicia o processo de rastreamento.

    :param productName: O nome do produto para fazer scraping.
    """
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    })

    process.crawl(AuchanSpider, product=productName)
    process.start()

def scrapeAuchan(productName):
    """
    Esta função é responsável por iniciar um processo separado para fazer scraping dos detalhes de um produto específico do site da Auchan, carregar os dados do arquivo 'output.json', remover o arquivo 'output.json' e filtrar os dados.

    1. A função inicia um processo separado que executa a função 'scrapeAuchanProcess' com o nome do produto como argumento.
    2. A função espera o processo terminar.
    3. A função abre o arquivo 'output.json', carrega os dados em formato JSON e imprime os dados.
    4. A função remove o arquivo 'output.json'.
    5. A função filtra os dados para remover quaisquer itens que contenham valores None.
    6. A função retorna os dados filtrados.

    :param productName: O nome do produto para fazer scraping.
    :return: Uma lista de dicionários contendo os detalhes do produto.
    """
    p = Process(target=scrapeAuchanProcess, args=(productName,))
    p.start()
    p.join()
    
    print("================================================")
    print("O spider deu:\n")
    
    with open('output.json', 'r') as file:
        data = json.load(file)
        print(data)
    print("================================================")

    if os.path.exists("output.json"):
        os.remove("output.json")

    data = [item for item in data if None not in item.values()]
    
    return data

def scrapeAuchanProductProcess(productLink):
    """
    Esta função é responsável por iniciar um processo de rastreamento para fazer scraping dos detalhes de um produto específico do site da Auchan usando o link do produto.

    1. A função inicializa um processo de rastreamento com um agente de usuário específico e configurações de saída.
    2. A função inicia um rastreamento do Spider da Auchan com o link do produto como argumento.
    3. A função inicia o processo de rastreamento.

    :param productLink: O link do produto para fazer scraping.
    """
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    })

    process.crawl(AuchanProductSpider, productLink=productLink)
    process.start()

def scrapeAuchanProduct(productLink):
    """
    Esta função é responsável por iniciar um processo separado para fazer scraping dos detalhes de um produto específico do site da Auchan usando o link do produto, carregar os dados do arquivo 'output.json', remover o arquivo 'output.json' e filtrar os dados.

    1. A função inicia um processo separado que executa a função 'scrapeAuchanProductProcess' com o link do produto como argumento.
    2. A função espera o processo terminar.
    3. A função abre o arquivo 'output.json', carrega os dados em formato JSON e imprime os dados.
    4. A função remove o arquivo 'output.json'.
    5. A função filtra os dados para remover quaisquer itens que contenham valores None.
    6. A função retorna os dados filtrados.

    :param productLink: O link do produto para fazer scraping.
    :return: Uma lista de dicionários contendo os detalhes do produto.
    """
    p = Process(target=scrapeAuchanProductProcess, args=(productLink,))
    p.start()
    p.join()

    print("================================================")
    print("O spider deu:\n")
    
    with open('output.json', 'r') as file:
        data = json.load(file)
        print(data)
    print("================================================")

    if os.path.exists("output.json"):
        os.remove("output.json")

    data = [item for item in data if None not in item.values()]
    
    return data

# A main foi usada somente para testes:
if __name__ == "__main__":
    #product = input("Choose the product you want to scrape from Amazon: ")
    #items = scrapeAmazon(product)
    #
    ##write data in .json file
    #with open('My.json', 'w') as file:
    #    json.dump(items, file)
    
    #product = "leite"
    #items = scrapeAuchan(product)
    
    productLink = "https://www.auchan.pt/pt/produtos-frescos/padaria/pao-fresco-e-broa/pao-alentejano-de-cabrela-forma-fatiado-400g-produto-local/768626.html"
    print("A fazer scrape do produto:" + str(productLink))
    items = scrapeAuchanProduct(productLink)
    
    #write data in .json file
    with open('TESTE_SCRAPING.json', 'w') as file:
        json.dump(items, file)
