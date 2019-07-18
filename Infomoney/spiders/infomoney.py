# -*- coding: utf-8 -*-
import scrapy

import re
import unicodedata

class InfomoneySpider(scrapy.Spider):

    name = 'infomoney'
    start_urls = ['https://www.infomoney.com.br/cryptos/ultimas-noticias']

    def parse(self, response):
        links = response.css('div.section-box-secondary-container-description a::attr(href)').getall()

        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_craw
                )

        next_page = response.css('li.arrow a::attr(href)').getall()

        yield scrapy.Request(
            response.urljoin(next_page[-1]),
            callback=self.parse
            )

    def parse_craw(self, response):
        # title = response.css('section h1::text').get()
        date_news = response.css('div.row.article__info.show-for-large span::attr(data-date)').get()
        text_news = ' '.join(response.xpath('//div[@class="article__content"]/p/text()').getall())
        user_news = 'Info Money'

        text_news = self.clean_text(text_news) 

        yield{
            # 'title': title,
            'date_news': date_news,
            'text_news': text_news,
            'user_news': user_news
        }

    def clean_text(self, text):
        
        # Unicode normalize transforma um caracter em seu equivalente em latin.
        nfkd = unicodedata.normalize('NFKD', text)
        word_without_accent = u"".join([c for c in nfkd if not unicodedata.combining(c)])

        # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
        return re.sub("(@ [A-Za-z0-9]+)|([^0-9A-Za-z $])|(\w+:\/\/\S+)", "", word_without_accent)