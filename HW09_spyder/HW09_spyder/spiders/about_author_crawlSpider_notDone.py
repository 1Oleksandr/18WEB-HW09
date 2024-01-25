import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AboutAuthorSpider(CrawlSpider):
    name = "about_author"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    rules = (
        # Rule(
        #     LinkExtractor(allow=('page', ), deny=('tag',)), callback='parse'
        # ),
        Rule(LinkExtractor(allow=('author', )), callback='parse_authors'),

    )

    # def parse(self, response):
    #     next_link = response.xpath("//li[@class='next']/a/@href").get()
    #     if next_link:
    #         yield scrapy.Request(url=self.start_urls[0] + next_link)
    # next_link = response.xpath("//li[@class='next']/a/@href").get()
    # if next_link:
    #     yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_authors(self, response):

        yield {
            "author": response.xpath("/html//h3[@class='author-title']/text()").get(),
            "born_date": response.xpath("/html//span[@class='author-born-date']/text()").get(),
            "born_location": response.xpath("/html//span[@class='author-born-location']/text()").get(),
            "description": response.xpath("/html//div[@class='author-description']/text()").get()
        }


# class DnsUltrabookSpider(scrapy.Spider):
#     name = 'dns_ultrabook'
#     allowed_domains = ['dns-shop.ru']
#     start_urls = [
#         'https://www.dns-shop.ru/catalog/17a892f816404e77/?f[65c]=264d&p=1']

#     def parse(self, response):
#         # Give data of css
#         product_name = response.css(
#             '.product-info__title-link > a::text').extract()
#         product_info = response.css(
#             '.product-info__title-description::text').extract()
#         product_url = response.css(
#             '.product-info__title-link > a::attr(href)').extract()
#         full_product_url = []
#         for url in product_url:
#             full_product_url.append("https://www.dns-shop.ru" + url)
#         for i in range(len(full_product_url)):
#             yield scrapy.Request(full_product_url[i], callback=self.price_parse,
#                                  meta={'product_name': product_name[i],
#                                        'product_info': product_info[i],
#                                        'product_url': full_product_url[i]})

#     def price_parse(self, response):
#         price = response.xpath(
#             '//span[@class="current-price-value"]//text()').extract_first()
#         scrap_info = {
#             'product_name': response.meta['product_name'],
#             'product_info': response.meta['product_info'],
#             'product_url': response.meta['product_url'],
#             'price': price
#         }
#         return scrap_info
