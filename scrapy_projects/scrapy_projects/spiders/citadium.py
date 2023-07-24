import copy
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from scrapy_projects.items import ScrapyProjectsItem


class CitadiumSpider(CrawlSpider):
    name = "citadium"
    allowed_domains = ["www.citadium.com"]
    start_urls = ["https://www.citadium.com/fr/fr"]
    css_links = [".change-bg-anim a", "li.container-submenu a.link_style-1", "div.letter-header a"]
    rules = (
        Rule(LinkExtractor(restrict_css=css_links),
             process_request="add_trail_and_follow", follow=True),

        Rule(LinkExtractor(restrict_css="#view-all-items .position-relative"),
             process_request="add_trail_and_follow", callback="parse_products", follow=False)
    )

    def add_trail_and_follow(self, request, response):
        request.meta.update({"trail": self.get_updated_trail(response)})
        return request

    def parse_products(self, response):

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
        item["trail"] = self.get_updated_trail(response)
        item["url"] = self.extract_product_url(response)

        yield item

    def extract_page_name(self, response):
        page_names = response.css("div.block-breadcrum span[itemprop='name']::text").getall()
        return page_names[-1].strip() if page_names else ""

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
        return response.css(".w-100.lzy_img.d-none::attr(src)").getall()

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
        script_content = response.css("script[type='application/ld+json']::text").get()
        json_data = json.loads(script_content)

        skus = {}
        for offer in json_data.get("offers", []):
            sku = offer.get("sku")
            colour = offer.get("colour")
            currency = offer.get("priceCurrency")
            price = offer.get("price")
            size = offer.get("size")

            if sku:
                skus[sku] = {
                    "colour": colour,
                    "currency": currency,
                    "price": price,
                    "size": size,
                }

        return skus

    def extract_product_url(self, response):
        return response.css("link[rel='canonical']::attr(href)").get()

    def get_updated_trail(self, response):
        page_name = self.extract_page_name(response)
        url = response.url
        trail = copy.deepcopy(response.meta.get("trail", []))
        trail.append([page_name, url])

        return trail

