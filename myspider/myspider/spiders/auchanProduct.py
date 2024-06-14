import scrapy
from ..items import SpiderAuchanProductItem

class AuchanProductSpider(scrapy.Spider):
    """
    Uma classe Spider do Scrapy para raspar dados de um produto específico do site Auchan.
    """
    name = "auchan_spider"
    product = ''
    start_urls = []

    def __init__(self, productLink: str = None, *args, **kwargs):
        """
        Inicializa a spider com o link do produto a ser pesquisado.

        Args:
            productLink (str): O link do produto a ser pesquisado no site Auchan.
        """
        super().__init__(*args, **kwargs)
        self.start_urls = [productLink]

    def parse(self, response):
        """
        Analisa a resposta do site Auchan.

        Args:
            response (scrapy.http.Response): O objeto de resposta a ser analisado.

        Yields:
            SpiderAuchanProductItem: Os dados do produto raspados.
        """
        container = response.css('div.col-12.value.content.auc-pdp__accordion-body.auc-pdp__attribute-container')
        product_data = {}
        item = SpiderAuchanProductItem()
        for section in container:
            headers = section.css('h3.attribute-name.auc-pdp-attribute-title::text').getall()
            for header in headers:
                ul = section.xpath(f'//h3[text()="{header}"]/following-sibling::ul[1]')
                if ul:
                    li_text = ul.css('li::text').get()
                    product_data[header.strip()] = li_text.strip() if li_text else None
        
        print("== O scrape dos produtos da Auchan ============")
        print(product_data)
        print("================================================")
        
        item['infos'] = product_data
        yield item