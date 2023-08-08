import copy
import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from scrapy_projects.items import ScrapyProjectsItem


class ParsingSpider(CrawlSpider):
    name = "citadium_parser"

    def parse_product(self, response):
        item = ScrapyProjectsItem()
        item["brand"] = self.extract_product_brand(response)
        item["category"] = self.extract_product_category(response)
        item["currency"] = self.extract_product_currency(response)
        item["description"] = self.extract_product_description(response)
        item["gender"] = self.extract_product_gender(response)
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
        return response.css("p.align-items-center::text").get().strip()

    def extract_product_category(self, response):
        return response.css(".product-infos-text-seo a::text").getall()

    def extract_product_currency(self, response):
        return response.css("script::text").re_first(r'"priceCurrency":"(\w+)"')

    def extract_product_description(self, response):
        return [text.strip().replace("-", "")
                for text in response.css(".op-tab-0::text").getall()
                if text.strip()]

    def extract_product_gender(self, response):
        return response.css("li:nth-child(2) [itemprop='name']::text").get()

    def extract_product_image_urls(self, response):
        script_content = response.css("script[type='application/ld+json']::text").get()
        return json.loads(script_content).get("image")

    def extract_product_language(self, response):
        return response.css("html::attr(lang)").get().split("-")[0]

    def extract_product_market(self, response):
        return response.css("html::attr(lang)").get().split("-")[1]

    def extract_product_name(self, response):
        return response.css("h1::text")[1].getall()[0].strip()

    def extract_product_price(self, response):
        price = response.css(".text_style-11 span::text").get().split("\xa0")[0].replace(",", ".")
        return eval(price)

    def extract_product_retailer_sku(self, response):
        return response.css("link[rel='canonical']::attr(href)").get().split("-")[-1]

    def extract_product_skus(self, response):
        script_content = re.findall(r'dataLayer\.push\((\{.*?\})\);',
                                    response.xpath("//script")[1].extract())
        json_data = json.loads(script_content[1])

        skus = {}
        product = json_data.get("ecommerce", {}).get("detail", {}).get("products", [])[0]
        variants = product.get("sizes", [])

        for variant in variants:
            sku_id = variant.get("refId")
            price = eval(variant.get("price"))
            size = variant.get("size").replace(",", ".")
            out_of_stock = not variant.get("quantity")

            skus[sku_id] = {
                "color": response.css(".active-color::text").get(),
                "currency": self.extract_product_currency(response),
                "price": price,
                "size": "One Size" if size == "TU" else size,
                "out_of_stock": out_of_stock
                }

        return skus

    def extract_product_url(self, response):
        return response.css("[rel='canonical']::attr(href)").get()


class CrawlingSpider(CrawlSpider):
    name = "citadium"
    allowed_domains = ["www.citadium.com"]
    start_urls = ["https://www.citadium.com/fr/fr"]

    listings_css = [
        ".change-bg-anim a",
        ".container-submenu .link_style-1",
        "[rel='next']",
        ".letter-header a",
    ]
    products_css = [
        "#view-all-items .position-relative",
        ".swiper-container-colors li a",
    ]

    parsing_spider = ParsingSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css),
             process_request="add_trail_and_follow"),
        Rule(LinkExtractor(restrict_css=products_css),
             process_request="add_trail_and_follow", callback=parsing_spider.parse_product),
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
