from copy import deepcopy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from scrapy_projects.spiders.parsing_spider import ParsingSpider


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
             process_request="add_trail_and_follow", callback=parsing_spider.parse_product),
    )

    def add_trail_and_follow(self, request, response):
        request.meta.update({"trail": self.get_updated_trail(response)})
        return request

    def extract_page_name(self, response):
        page_name = response.css("title::text").get()
        return page_name

    def get_updated_trail(self, response):
        page_name = self.extract_page_name(response)
        url = response.url
        trail = deepcopy(response.meta.get("trail", []))
        trail.append([page_name, url])

        return trail
