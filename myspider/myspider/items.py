# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MyspiderItem(scrapy.Item):
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_score = scrapy.Field()
    product_nscore = scrapy.Field()
    product_imgurl = scrapy.Field()
    product_link = scrapy.Field()
    pass

class SpiderAuchanItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    pass

class SpiderAuchanProductItem(scrapy.Item):
    infos = scrapy.Field()
    pass