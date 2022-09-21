import scrapy
from bs4 import BeautifulSoup
import pandas


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://rezka.ag/series/comedy/2040-kremnievaya-dolina-2014.html',
            'https://rezka.ag/series/adventures/51336-sezon-svadeb-2022.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = response.url.split('/')[-1].replace('.html', '')
        soup = BeautifulSoup(response.body, 'lxml')
        try:
            title = soup.find(class_='b-post__title').text.strip()
        except:
            title = '-'
        try:
            origtitle = soup.find(class_='b-post__origtitle').text
        except:
            origtitle = '-'
        try:
            imdb = soup.find_all(class_='bold')[0].text
        except:
            imdb = '-'
        try:
            country = soup.find(class_='b-post__info').text.split('Страна: ')[1].split(' ')[0]
        except:
            country = '-'
        try:
            duration = soup.find(class_='b-post__info').text.split('Время: ')[1].split('. ')[0] + '.'
        except:
            duration = '-'
        try:
            description = soup.find(class_='b-post__description_text').text
        except:
            description = '-'
        data = {'title': [title], 'origtitle': [origtitle], 'imdb': [imdb],
                'country': [country], 'duration': [duration], 'description': [description]}
        self.write_in_csv(data, filename)
        return self.read_csv(filename)

    def write_in_csv(self, data, filename):
        dataframe = pandas.DataFrame(data)
        dataframe.to_csv(f'{filename}.csv', index=False, sep=';')

    def read_csv(self, filename):
        res = pandas.read_csv(f'{filename}.csv')
        return res

