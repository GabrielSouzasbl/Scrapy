# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


class InfomoneyPipeline(object):

    def process_item(self, item, spider):

        self.cursor.execute(
            'INSERT INTO noticias(data, texto, usuario) VALUES(%(date_news)s, %(text_news)s, %(user_news)s)',
            item
        )
        self.cursor.commit()

        return item

    def open_spider(self, spider):
        try:
            self.connection = psycopg2.connect("dbname='bd_bitcoin' user='postgres' host='localhost' password='99391292' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            print("Cannot connect to database")

    def close_spider(self, spider):
        self.cursor.close()  
