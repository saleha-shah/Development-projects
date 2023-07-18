# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjectsItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
