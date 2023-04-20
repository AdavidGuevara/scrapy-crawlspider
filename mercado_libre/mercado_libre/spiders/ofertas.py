from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class OfertasSpider(CrawlSpider):
    name = "ofertas"
    allowed_domains = ["mercadolibre.com.co"]
    start_urls = ["https://www.mercadolibre.com.co/ofertas"]
    custom_settings = {
        "FEED_URI": "ofertas.json",
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    rules = (
        Rule(
            LinkExtractor(allow=r"container_id=MCO779366-1&page="),
            callback="parse_item",
        ),
    )

    def parse_item(self, response):
        items = response.xpath(
            '//li[contains(@class, "promotion-item")]//div/a/div/div[2]'
        )
        for item in items:
            yield {
                "titulo": item.xpath('./p/text()').get(),
                "precio": item.xpath('./div[contains(@class, "item__price")]/div/span[1]/span[contains(@class, "fraction")]/text()').get(),
                "descuento": item.xpath('./div[contains(@class, "item__price")]/div/span[2]/text()').get(),
            }
