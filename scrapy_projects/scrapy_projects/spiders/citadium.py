from scrapy import Spider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_projects.items import ScrapyProjectsItem


class CitadiumSpider(Spider):
    name = "citadium"
    allowed_domains = ["www.citadium.com"]
    start_urls = ["https://www.citadium.com/fr/fr/femme"]
    rules = (
        Rule(LinkExtractor(allow='page/', deny='tag/'), callback='parse_product_links', follow=True),
    )

    def parse(self, response):
        url = response.css("li.container-submenu a.link_style-1::attr(href)")[1].get()
        yield response.follow(url, self.parse_brand_links)
        yield from self.parse_product_links(response)

    def parse_brand_links(self, response):
        for brand_url in response.css("div.letter-header a::attr(href)").getall():
            yield response.follow(brand_url, self.parse_product_links)

    def parse_product_links(self, response):
        for product_url in response.css("#view-all-items .position-relative::attr(href)").getall():
            yield response.follow(product_url, self.parse_products)

    def parse_products(self, response):
        item = ScrapyProjectsItem()
        item["brand"] = response.css("p.align-items-center::text").get().strip()
        item["category"] = response.css('div.product-infos-text-seo span a::text').getall()
        item["currency"] = response.css("script::text").re_first(r'"priceCurrency":"(\w+)"')
        item["description"] = [text.strip().replace('-', '')
                               for text in response.css("div.op-tab-0::text").getall() 
                               if text.strip()]
        item["gender"] = response.css("div#ariane li:nth-child(2) span::text").get()
        item["image_urls"] = response.css(".w-100.lzy_img.d-none::attr(src)").getall()
        item["lang"] = response.css("html::attr(lang)").get().split("-")[0]
        item["market"] = response.css("html::attr(lang)").get().split("-")[1]
        item["name"] = response.css("h1.fs-18.mb-3.d-flex.flex-column::text")[1].getall()[0].strip()
        item["price"] = response.css("p.text_style-11 span::text").get().split("\xa0")[0].replace(",", ".")
        item["retailer_sku"] = response.css("link[rel='canonical']::attr(href)").get().split("-")[-1]
        item["trail"] = [[element.css('span::text').get().strip(), element.css('a::attr(href)').get()] 
                         if element.css('a') else element.css('span::text').get().strip() 
                         for element in response.css('.block-breadcrum [itemprop="itemListElement"]')]
        item["url"] = response.css("link[rel='canonical']::attr(href)").get()
        yield item
