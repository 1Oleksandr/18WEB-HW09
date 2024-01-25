import scrapy
# from scrapy.crawler import CrawlerProcess
from scrapy.http import Request

tags = []


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json",
                       "FEED_URI": "quotes_authors.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        # Получаем все цитаты, их авторов и теги с одной страницы

        author_name = response.xpath("//span/small/text()").getall()
        quote = response.xpath("//span[@class='text']/text()").getall()
        for tag in response.xpath("/html//div[@class='quote']"):
            tags.append(tag.xpath("div[@class='tags']/a/text()").getall())

        # Получаем ссылки на описание всех авторов с одной страницы
        author_url = response.xpath(
            "//div[@class='quote']//span/a/@href").getall()
        authors_url = []
        for url in author_url:
            authors_url.append(self.start_urls[0] + url)
        # Добавляем в словарь Имя автора, цитату и ссылку и вызываем через
        # callback функцию, которая скрапит страницу об авторе и добавляет
        # в словарь данные об авторе
        for i in range(len(authors_url)):
            yield scrapy.Request(authors_url[i], callback=self.author_parse,
                                 meta={'author_name': author_name[i],
                                       'quote': quote[i],
                                       'tags': tags[i]
                                       })
        # Переходим на следующую страницу пока она существует
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def author_parse(self, response):
        # Убираем из описагия автора переносы строки и пробелы
        desc = response.xpath(
            "/html//div[@class='author-description']/text()").get()
        description = desc.strip()

        scrap_info = {
            "author": response.meta['author_name'],
            "quote": response.meta['quote'],
            "tags": response.meta['tags'],
            # "author_name": response.xpath("/html//h3[@class='author-title']/text()").get(),
            "born_date": response.xpath("/html//span[@class='author-born-date']/text()").get(),
            "born_location": response.xpath("/html//span[@class='author-born-location']/text()").get(),
            "description": description,
        }
        # Возвращаем данные в parse
        return scrap_info
