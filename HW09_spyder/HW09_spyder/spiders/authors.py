# from typing import Iterable
import scrapy
from scrapy.http import Request


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotess.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):

        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


# run spider
# process = CrawlerProcess()
# process.crawl(QuotesSpider)
# process.start()
