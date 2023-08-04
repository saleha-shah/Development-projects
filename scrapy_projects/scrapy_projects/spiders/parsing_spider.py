from copy import deepcopy
from json import loads
from re import findall

from scrapy import Request
from scrapy.spiders import CrawlSpider

from scrapy_projects.items import ScrapyProjectsItem


class ParsingSpider(CrawlSpider):
    name = "damsel_parser"
    allowed_domains = ["www.damselinadress.com"]

    def parse_product(self, response):
        item = ScrapyProjectsItem()
        item["brand"] = self.extract_product_brand(response)
        item["category"] = self.extract_product_category(response)
        item["currency"] = self.extract_product_currency(response)
        item["description"] = self.extract_product_description(response)
        # item["gender"] = self.extract_product_gender(response)
        item["image_urls"] = self.extract_product_image_urls(response)
        item["lang"] = self.extract_product_language(response)
        item["market"] = self.extract_product_market(response)
        item["name"] = self.extract_product_name(response)
        item["price"] = self.extract_product_price(response)
        item["retailer_sku"] = self.extract_product_retailer_sku(response)
        # item["skus"] = self.extract_product_skus(response)
        item["trail"] = deepcopy(response.meta.get("trail", []))
        item["url"] = self.extract_product_url(response)
        skus_requests = self.extract_product_skus(response)
        for request in skus_requests:
            yield request

        # yield item

    def extract_product_brand(self, response):
        return response.css(".product-detail__brand-name::text").get()

    def extract_product_category(self, response):
        return [item.strip() for item in response.css(".breadcrumb-item a::text")[1:].getall()]

    def extract_product_currency(self, response):
        return response.css("script::text").re_first(r'"currency":"(\w+)"')

    def extract_product_description(self, response):
        return [item.strip() for item in response.css(".card-body")[0].css("::text").getall()
                if item.strip()]

    # def extract_product_gender(self, response):
        # return response.css("div#ariane li:nth-child(2) span[itemprop='name']::text").get()

    def extract_product_image_urls(self, response):
        return response.css(".zoom-image::attr(src)").getall()

    def extract_product_language(self, response):
        return response.css("script::text").re_first(r'"language":"(\w+)"')

    def extract_product_market(self, response):
        return response.css("script::text").re_first(r'"country":"(\w+)"')

    def extract_product_name(self, response):
        return response.css("span[class*='product-name']::text").get().strip()
        # return response.css(".product-detail__product-name--text::text").get().strip()

    def extract_product_price(self, response):
        return eval(response.css("script::text").re_first(r'"price":"(\w+)"'))

    def extract_product_retailer_sku(self, response):
        return response.css("script::text").re_first(r'"id":"(\w+)"')

    def extract_product_skus(self, response):
        links = response.css('.product-detail__attribute__value[data-attr="color"].product-detail__attribute__value--low-stock.product-detail__attribute__value--selectable::attr(data-action)').getall()
        requests = []

        for link in links:
            skus_request = Request(url=link, callback=self.parse_dynamic_data, meta={'item': deepcopy(response.meta.get("item", {}))})
            requests.append(skus_request)
        
        return requests

    
    def extract_product_url(self, response):
        return response.css("link[rel='canonical']::attr(href)").get()
    
    def parse_dynamic_data(self, response):
        size_elements = response.css('.product-detail__attribute__value[data-attr="size"]')

        # Initialize the dictionary to store the skus
        skus = {}
        color = response.css(".product-detail__attribute__value--current::attr(data-tippy-content)").get() 
        # Iterate over each size option element
        for size_element in size_elements:
            # color = size_element.css('p::attr(data-action)').re_first(r'_color=(\d+)')
            size = size_element.css('p::attr(data-value)').get()
            out_of_stock = "Out of Stock" in size_element.css('p::attr(data-tippy-content)').get()

            if color and size:
                sku_key = f"{color}_{size}"
                skus[sku_key] = {
                    'colour': color,
                    'size': size,
                    'out_of_stock': out_of_stock
                }

        item = response.meta['item']
        item['skus'] = skus
        yield item
