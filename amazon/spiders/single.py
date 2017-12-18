# -*- coding: utf-8 -*-
import random

import scrapy
import MySQLdb
from scrapy import Request

from amazon.Database import Database
from amazon.items import AmazonItem


class SingleSpider(scrapy.Spider):
    name = 'single'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']

    def __init__(self, *args, **kwargs):
        super(SingleSpider, self).__init__(*args, **kwargs)
        self.proxy_pool = ["35.194.82.128:80", "149.202.180.55:3128", "147.135.210.114:54566", "117.141.18.70:54132",
                           "124.195.19.18:808", "52.170.21.0:3128", "35.196.219.234:80", "85.91.96.56:8080",
                           "35.196.28.24:80", "78.120.139.47:3128", "104.196.206.179:80", "118.69.140.108:53281",
                           "165.84.167.54:8080", "35.227.22.80:80", "35.227.62.48:80", "151.80.140.233:54566",
                           "46.254.203.15:8080", "45.6.216.66:80", "34.216.164.128:3128", "192.116.142.153:8080",
                           "119.178.221.210:8118", "13.78.125.167:8080", "35.227.36.184:80", "35.196.225.14:80",
                           "118.69.57.180:53281", "120.199.64.163:808", "52.224.181.154:3128", "124.104.113.255:8080",
                           "138.68.156.224:8118", "92.42.109.43:1080", "86.244.199.24:21320", "201.151.178.235:8080",
                           "61.7.231.22:8080", "41.193.222.58:3128", "35.227.67.169:80", "89.236.17.106:3128",
                           "139.59.160.94:8118", "120.33.247.123:808", "47.88.32.46:3128", "110.77.181.140:65205",
                           "5.196.189.50:8080", "178.44.255.232:8080", "188.254.78.108:8080", "173.212.228.42:10059"]

    def parse(self, response):
        item = AmazonItem()
        if len(response.css("input#ASIN,#imgTagWrapperId,#imageBlockContainer").extract()):
            item['html'] = response.body
            item['code'] = response.meta['id']
            return item
        return None

    def start_requests(self):
        # execute SQL query using execute() method.
        cursor = Database.cursor()
        cursor.execute("SELECT code FROM sonic where crawled = 0")

        for row in cursor:
            url = "https://www.amazon.com/dp/%s" % row
            proxy = random.choice(self.proxy_pool)
            yield Request(url, dont_filter=True, meta={"id": row[0], "proxy":proxy}, headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36'
            })
