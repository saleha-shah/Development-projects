import copy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from scrapy_projects.items import ScrapyProjectsItem


class ParsingSpider(CrawlSpider):
    name = "damsel_parser"

    def parse(self, response):
        item = ScrapyProjectsItem()
        item["brand"] = self.extract_product_brand(response)
        item["care"] = self.extract_product_care(response)
        item["category"] = self.extract_product_category(response)
        item["currency"] = self.extract_product_currency(response)
        item["description"] = self.extract_product_description(response)
        item["image_urls"] = self.extract_product_image_urls(response)
        item["lang"] = self.extract_product_language(response)
        item["market"] = self.extract_product_market(response)
        item["name"] = self.extract_product_name(response)
        item["price"] = self.extract_product_price(response)
        item["retailer_sku"] = self.extract_product_retailer_sku(response)
        item["skus"] = self.extract_product_skus(response)
        item["trail"] = copy.deepcopy(response.meta.get("trail", []))
        item["url"] = self.extract_product_url(response)

        yield item

    def extract_product_brand(self, response):
        return response.css(".product-detail__brand-name::text").get()

    def extract_product_care(self, response):
        return response.css("#collapseTwo li::text")[1].get().split(":")[1].strip()

    def extract_product_category(self, response):
        return [item.strip() for item in response.css(".breadcrumb-item a::text")[1:].getall()]

    def extract_product_currency(self, response):
        return response.css("script::text").re_first(r'"currency":"(\w+)"')

    def extract_product_description(self, response):
        return [item.strip() for item in response.css(".card-body")[0].css("::text").getall()
                if item.strip()]

    def extract_product_image_urls(self, response):
        return response.css(".zoom-image::attr(src)").getall()

    def extract_product_language(self, response):
        return response.css("script::text").re_first(r'"language":"(\w+)"')

    def extract_product_market(self, response):
        return response.css("script::text").re_first(r'"country":"(\w+)"')

    def extract_product_name(self, response):
        return response.css(".product-detail__product-name--text::text").get().strip()

    def extract_product_price(self, response):
        return eval(response.css(".value::text").get().strip()[1:])

    def extract_product_retailer_sku(self, response):
        return response.css("script::text").re_first(r'"id":"(\w+)"')

    def extract_product_url(self, response):
        return response.css("link[rel='canonical']::attr(href)").get()

    def extract_product_skus(self, response):
        size_elements = response.css("[data-attr='size']")
        skus = {}
        color = response.css(".product-detail__attribute__display-value::text").get().strip()

        for size_element in size_elements:
            size = size_element.css("::attr(data-value)").get()
            out_of_stock = "Out of Stock" in size_element.css("::attr(data-tippy-content)").get()

            sku_key = f"{color}_{size}"
            skus[sku_key] = {
                "colour": color,
                "size": size,
                "currency": self.extract_product_currency(response),
                "price": self.extract_product_price(response),
                "out_of_stock": out_of_stock,
            }

        return skus


class CrawlingSpider(CrawlSpider):
    name = "damsel"
    allowed_domains = ["www.damselinadress.com"]
    start_urls = ["https://www.damselinadress.com"]

    listings_css = [
        "li.d-lg-block a",
    ]
    products_css = [
        ".pdp-link a",
    ]

    parsing_spider = ParsingSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css),
             process_request="add_trail_and_follow"),
        Rule(LinkExtractor(restrict_css=products_css),
             process_request="add_trail_and_follow", callback=parsing_spider.parse),
    )

    def add_trail_and_follow(self, request, response):
        request.meta.update({"trail": self.get_updated_trail(response)})
        return request

    def extract_page_name(self, response):
        return response.css("title::text").get()

    def get_updated_trail(self, response):
        page_name = self.extract_page_name(response)
        url = response.url
        trail = copy.deepcopy(response.meta.get("trail", []))
        trail.append([page_name, url])

        return trail
