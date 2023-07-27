from copy import deepcopy
from json import loads
from re import findall


from scrapy.spiders import CrawlSpider
from scrapy import Request

from scrapy_projects.items import ScrapyProjectsItem


class ParsingSpider(CrawlSpider):
    allowed_domains = ["www.citadium.com"]
    name = "citadium_parser"

    def parse_products(self, response):
        urls = response.css("div.swiper-container-colors li a::attr(href)").getall()
        for url in urls:
            yield Request(url=url, callback=self.extract_product_info,
                          method="GET", meta={"trail": response.meta.get("trail", [])})

    def extract_product_info(self, response):
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
        item["trail"] = deepcopy(response.meta.get("trail", []))
        item["url"] = self.extract_product_url(response)

        yield item

    def extract_product_brand(self, response):
        return response.css("p.align-items-center::text").get().strip()

    def extract_product_category(self, response):
        return response.css("div.product-infos-text-seo span a::text").getall()

    def extract_product_currency(self, response):
        return response.css("script::text").re_first(r'"priceCurrency":"(\w+)"')

    def extract_product_description(self, response):
        return [text.strip().replace("-", "")
                for text in response.css("div.op-tab-0::text").getall()
                if text.strip()]

    def extract_product_gender(self, response):
        return response.css("div#ariane li:nth-child(2) span[itemprop='name']::text").get()

    def extract_product_image_urls(self, response):
        script_content = response.css("script[type='application/ld+json']::text").get()
        json_data = loads(script_content)
        return json_data.get("image")

    def extract_product_language(self, response):
        return response.css("html::attr(lang)").get().split("-")[0]

    def extract_product_market(self, response):
        return response.css("html::attr(lang)").get().split("-")[1]

    def extract_product_name(self, response):
        return response.css("h1.fs-18.mb-3.d-flex.flex-column::text")[1].getall()[0].strip()

    def extract_product_price(self, response):
        return response.css("p.text_style-11 span::text").get().split("\xa0")[0].replace(",", ".")

    def extract_product_retailer_sku(self, response):
        return response.css("link[rel='canonical']::attr(href)").get().split("-")[-1]

    def extract_product_skus(self, response):
        html_content = response.text
        script_content = findall(r"dataLayer\.push\((\{.*?\})\);", html_content)

        if script_content:
            json_data = loads(script_content[1])
            skus = {}
            product = json_data.get("ecommerce", {}).get("detail", {}).get("products", [])[0]
            variants = product.get("sizes", [])
            for variant in variants:
                sku_id = variant.get("refId")
                price = variant.get("price")
                size = variant.get("size").replace(",", ".")
                quantity = False if variant.get("quantity") else True

                skus[sku_id] = {
                    "color": response.css("p.active-color::text").get(),
                    "currency": self.extract_product_currency(response),
                    "price": price,
                    "size": "One Size" if size == "TU" else size,
                    "out_of_stock": quantity
                    }

        return skus

    def extract_product_url(self, response):
        return response.css("link[rel='canonical']::attr(href)").get()
