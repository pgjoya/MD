import scrapy
from ..items import SpiderAuchanItem

class AuchanSpider(scrapy.Spider):
    """
    Uma classe Spider do Scrapy para raspar dados de produtos do site Auchan.
    """
    name = "auchan_spider"
    product = ''
    start_urls = []

    def __init__(self, product: str = None, *args, **kwargs):
        """
        Inicializa a spider com o produto a ser pesquisado.

        Args:
            product (str): O produto a ser pesquisado no site Auchan.
        """
        super().__init__(*args, **kwargs)
        self.product = product
        self.start_urls = [f"https://www.auchan.pt/pt/pesquisa?q={self.product}"]

    def parse(self, response):
        """
        Analisa a resposta do site Auchan.

        Args:
            response (scrapy.http.Response): O objeto de resposta a ser analisado.

        Yields:
            SpiderAuchanItem: Os dados do produto raspados.
        """
        products = response.css('div.product-tile')
        print("== Prints do Scrape ========================================")
        i = 0
        for product in products:
            
            items = SpiderAuchanItem()
            
            print(f"Product {i}")
            i += 1
            
            link = product.css('a.auc-product-tile__image-container__image::attr(href)').get()
            print(f"Link: {link}")
            
            name = product.css('div.auc-product-tile__name a.link::text').get() # CERTO
            print(f"Name: {name}")
            
            price = product.css('div.price .sales .value::text').get()
            price = price.replace('\n', '').replace('.', '').replace(',', '.').replace(' ', '')
            print(f"Price: {price}")
            print()
            print()
            
            items['link'] = link
            items['name'] = name
            items['price'] = price
            
            yield items
        print("============================================================")