# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from amazon.Database import Database


class AmazonPipeline(object):
    def process_item(self, item, spider):
        if item is None:
            return item

        cursor = Database.cursor()
        with open('data/'+item['code'] + '.html', 'w+') as my_file:
            my_file.write(item['html'])
        cursor.execute("UPDATE sonic set crawled=1 where code=%s", [item['code']])
        cursor.connection.commit()
        return item
