import json
import requests
from bs4 import BeautifulSoup


def parse_data(urla):
    try:
        html_doc = requests.get(urla)
        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            quotes = soup.select("[class*='quote']")
            for quote in quotes:
                text = quote.find(
                    'span', attrs={'class': 'text'}).text
                author = quote.find(
                    'small', attrs={'class': 'author'}).text
                tags = (quote.find('meta', attrs={'class': 'keywords'})[
                    'content']).split(',')
                store_.append({
                    'tags': tags,
                    'author': author,
                    'quote': text
                })
            next = soup.find('li', attrs={'class': 'next'}).find('a')['href']
            print(f'Scraping page{next}')
            parse_data(url+next)
        return store_
    except:
        print('Scraped all')


if __name__ == '__main__':
    url = 'https://quotes.toscrape.com'
    store_ = []

    store = parse_data(url)
    with open('quotes1.json', 'w', encoding="utf-8") as fd:
        fd.write(json.dumps(store))
