import scrapy

from ..items import ScrapyProjectsItem


class CitadiumSpider(scrapy.Spider):
    name = "citadium"
    allowed_domains = ["www.citadium.com"]
    start_urls = ["https://www.citadium.com/fr/fr/femme"]

    def parse(self, response):
        item = ScrapyProjectsItem()
        for index, product in enumerate(response.css("div.product-infos")):

            item["name"] = product.css("div > span::text").get()
            item["description"] = product.css("div > p::text").get().strip()

            color_css = product.css("div > p span::text")
            item["color"] = color_css.get() if color_css else None

            price_css = product.xpath(".//span[contains(text(), '€')]/text()")
            item["price"] = price_css.get().replace("\xa0", "").replace(",", ".")

            item["url"] = response.css("a.h-100.d-block.position-relative::attr(href)")[index].get()

            yield item
