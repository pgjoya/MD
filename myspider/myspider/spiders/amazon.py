from typing import Any
import scrapy
from ..items import MyspiderItem


class AmazonSpider(scrapy.Spider):
    name = "amazon_spider"
    product = 'milk'
    start_urls = [
        f"https://www.amazon.es/s?k=milk&i=grocery"
    ]

    def __init__(self, product: str = None, *args, **kwargs): #constructor
        super().__init__(*args, **kwargs)
        self.product = product
        self.start_urls = [f"https://www.amazon.es/s?k={product}&i=grocery&language=pt_PT&crid=2UZFITL2J6US5&sprefix=milk%2Cgrocery%2C169&ref=nb_sb_ss_ts-doa-p_1_4"]

    def parse(self,response):
        items = MyspiderItem()

        print("RESPONSE: " + response)

        products = response.css('div.puis-card-border')
        full_page = products.extract()
        for product in products:
            product_name = product.css('span.a-size-base-plus::text').get()
            product_price = product.css('.s-price-instructions-style .a-text-normal > .a-price .a-offscreen+ span').css('::text').extract()
            #product_price is a list of strings, so we need to join them
            product_price = ''.join(i for i in product_price)
            
            product_rating = product.css('.aok-align-bottom').css('::text').get()
            product_nrating = product.css('.s-link-style .s-underline-text::text').get()
            product_imgurl = product.css('.s-image-square-aspect .s-image::attr(src)').get()
            product_link ='https://amazon.es' + product.css('a.a-link-normal.s-no-outline::attr(href)').get()
            items['product_name'] = product_name
            items['product_price'] = product_price
            items['product_score'] = product_rating
            items['product_nscore'] = product_nrating
            items['product_imgurl'] = product_imgurl
            items['product_link'] = product_link

            yield items
