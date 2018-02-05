# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from amazon.libraries import Database


class MySQLPipeline(object):

    def process_item(self, item, spider):
        if item is not None:
            cursor = Database.cursor()
            connection = Database.get_connection()
            query = "INSERT INTO products " \
                    "(title, is_prime, reviews, category_id, code, rate, discount_percent, discount_price, original_price) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                    "ON DUPLICATE KEY UPDATE " \
                    "title=%s, is_prime=%s, reviews=%s, category_id=%s, rate=%s, " \
                    "discount_percent=%s, discount_price=%s, original_price=%s"
            params = [
                item['title'], item['is_prime'], item['reviews'], item['category_id'], item['code'], item['rate'],
                item['discount_percent'], item['discount_price'], item['original_price'],

                item['title'], item['is_prime'], item['reviews'], item['category_id'], item['rate'],
                item['discount_percent'], item['discount_price'], item['original_price']
            ]
            cursor.execute(query, params)
            connection.commit()
