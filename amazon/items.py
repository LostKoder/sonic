# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    code = scrapy.Field()
    rate = scrapy.Field()
    title = scrapy.Field()
    discount_percent = scrapy.Field()
    discount_price = scrapy.Field()
    original_price = scrapy.Field()
    category_id = scrapy.Field()
