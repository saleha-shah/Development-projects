from scrapy import Spider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_projects.items import ScrapyProjectsItem


class CitadiumSpider(Spider):
    name = "citadium"
    allowed_domains = ["www.citadium.com"]
    start_urls = ["https://www.citadium.com/fr/fr/femme",
                  "https://www.citadium.com/fr/fr/homme"]
    rules = (
        Rule(LinkExtractor(allow="page/", deny="tag/"), callback="parse_product_links", follow=True)
    )

    def parse(self, response):
        url = response.css("li.container-submenu a.link_style-1::attr(href)")[1].get()
        page_name = self.extract_page_name(response)

        yield response.follow(url, self.parse_brand_links, cb_kwargs={"trail": [[page_name, url]]})
        yield from self.parse_product_links(response, [[page_name, url]])

    def parse_brand_links(self, response, trail):
        page_name = self.extract_page_name(response)
        for brand_url in response.css("div.letter-header a::attr(href)").getall():
            yield response.follow(brand_url, self.parse_product_links,
                                  cb_kwargs={"trail": trail + [page_name, brand_url]})

    def parse_product_links(self, response, trail):
        page_name = self.extract_page_name(response)
        for product_url in response.css("#view-all-items .position-relative::attr(href)").getall():
            yield response.follow(product_url, self.parse_products,
                                  cb_kwargs={"trail": trail + [page_name, product_url]})

    def parse_products(self, response, trail):
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
        item["trail"] = trail
        item["url"] = self.extract_product_url(response)

        yield item

    def extract_page_name(self, response):
        page_names = response.css("div.block-breadcrum span[itemprop='name']::text").getall()
        if page_names:
            return page_names[-1].strip()
        return ""

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

    def extract_product_url(self, response):
        return response.css("link[rel='canonical']::attr(href)").get()
