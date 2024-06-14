# Grocery Helper - Trabalho de Mineração de Dados

## Membros do Projeto

-   PG52685: Joana Catarina Oliveira Gomes
-   PG54144: Pedro Marcelo Bogas Oliveira
-   PG54263: Tomás Cardoso Francisco

## Instruções para a execução do projeto

-   Para instalar todas as dependencias: `pip install -r requirements.txt --upgrade`
-   Para correr o flask: `flask --app GroceryHelper run`
-   Para correr o flask em modo debug: `flask --app GroceryHelper run --debug`

## Resumo do Projeto

Este projeto é uma aplicação web Flask que ajuda os utilizadores a obter informações sobre produtos de supermercado. Ele usa **web scraping** para coletar dados de produtos de sites de supermercado e a **API OpenAI** para responder a perguntas sobre os produtos selecionados.

### Web Scraping

-   O código em `myspider/myspider/spiders/auchan.py` define uma spider Scrapy que raspa dados de produtos do site Auchan.
-   As funções `scrapeAmazon`, `scrapeAuchan` e `scrapeAuchanProduct` em `webscraping.py` são usadas para raspar dados de produtos de diferentes sites e de produtos especificos.

### Flask App

O arquivo `GroceryHelper.py` define uma aplicação Flask com várias rotas.

1. **Rota '/' (home)**:

    - Método: GET
    - Função: Renderiza o template 'home.html'.
    - Descrição: Página inicial do aplicativo.

2. **Rota '/products'**:

    - Método: POST
    - Função: Extrai produtos alimentícios e bebidas de um texto usando OpenAI, faz scraping de detalhes desses produtos do site Auchan e renderiza um template com os produtos.
    - Descrição detalhada: Recebe um texto via POST, utiliza a API da OpenAI para extrair produtos, faz scraping dos detalhes desses produtos do Auchan, e renderiza o resultado no template 'products.html'.

3. **Rota '/productsSelection'**:

    - Método: POST
    - Função: Processa informações dos produtos selecionados, incluindo scraping de detalhes adicionais do site Auchan, se necessário, e renderiza um template com os produtos selecionados.
    - Descrição detalhada: Recebe informações dos produtos selecionados via POST, processa cada produto (incluindo scraping adicional se necessário), e depois renderiza o template 'questions.html' com os produtos processados.

4. **Rota '/submitQuestion'**:
    - Método: POST
    - Função: Recebe uma pergunta e a lista de produtos selecionados, utiliza a API da OpenAI para gerar uma resposta com base nesses produtos, e renderiza um template com a pergunta, resposta e produtos selecionados.
    - Descrição detalhada: Recebe uma pergunta e a lista de produtos selecionados, utiliza o ChatGPT da OpenAI para gerar uma resposta contextualizada com base nos produtos, e depois renderiza o template 'answer.html' com a pergunta, resposta e produtos.

Essas rotas formam um aplicativo Flask básico que utiliza Flask para servir páginas web com templates renderizados e integrações com APIs externas (OpenAI) e scraping de sites (Auchan).

### OpenAI API

-   O código em `GroceryHelper.py` também usa a API da OpenAI para extrair produtos de um texto fornecido e responder a perguntas sobre os produtos selecionados.

### Templates HTML

-   Existem vários templates HTML em `templates/` que são usados para renderizar diferentes partes da aplicação Flask.

### Arquivo de Configuração

-   O ficheiro `.env` é usado para armazenar a chave da API da OpenAI, no seguinte formato: "OPENAI_API_KEY=<key>"

Em resumo, a aplicação recebe um texto, extrai os produtos desse texto usando a API da OpenAI, faz web scraping dos detalhes de produtos de sites de supermercado e fornecer uma interface para o utilizador fazer perguntas sobre os produtos selecionados.
