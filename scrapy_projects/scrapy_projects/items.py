# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjectsItem(scrapy.Item):
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    currency = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    lang = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    trail = scrapy.Field()
    url = scrapy.Field()

