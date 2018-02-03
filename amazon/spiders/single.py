# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request, Selector

from amazon.libraries import Database
from amazon.items import Product


class SingleSpider(scrapy.Spider):
    name = 'single'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/']

    def __init__(self, *args, **kwargs):
        super(SingleSpider, self).__init__(*args, **kwargs)
        self.proxy_pool = []
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "session-id=131-0632311-7866820; session-id-time=2082787201l; ubid-main=134-8230983-4081137; x-wl-uid=1EAmqPwuI2990O8gtpou7A/V2ugDLLiO5o0B/pV+H1uzitXYeaVzkX7T8coL4w/+elp4dsV5HenU=; session-token=3i6pQdVcZXcF5BbJvMRl41CuDtWYhJMEI84VCX7+eTLeDHFMvwt8bQUwJJIlGzG1q95ma8L4c8pUTlOrJpz5RLrB7sxDYvdFF/srIV61qW+e6GKlYN09FAkgdRdSjIiRC6TBGWkUzPB3Z2wdDDUeO0OPw6GzSQjeSOMa2eS55e5MDrFAMF3ZEQKnTG/i8ZUmW0QZO/RkRA6xGmRhCTuNDeT0xSn+oFyJr0eePsmaxqOs5PL7MA6TM+OFRq6PQjsU; s_nr=1516441220147-New; s_vnum=1948441220147%26vn%3D1; s_dslv=1516441220148; skin=noskin; csm-hit=QPZ5W37C843R67D93HKX+s-NVYE8SC24X324VYNEFGM|1517651099354",
            "Host": "www.amazon.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",
        }

    def single_parse(self, response):
        search = re.search('(?:dp|o|gp|gp/product|-)/(B[0-9]{2}[0-9A-Z]{7}|[0-9]{9}(?:X|[0-9]))', response.url)
        selector = Selector(response)
        has_discount = len(selector.css('#regularprice_savings').extract()) > 0
        if search is not None and has_discount:
            product = Product()
            product['code'] = search.groups()[0]
            if len(selector.css('#acrPopover .a-icon-alt::text').extract()):
                product['rate'] = selector.css('#acrPopover .a-icon-alt::text').extract()[0].replace(" out of 5 stars", "")
            else:
                product['rate'] = '3'
            product['title'] = selector.css('#productTitle::text').extract()[0].strip()
            product['title'] = u' '.join((product['title'])).encode('utf-8').strip()
            product['discount_percent'] = re.sub('(^.*?\()|\)|%', '', selector.css("#regularprice_savings .a-color-price::text").extract()[0])
            product['discount_price'] = re.sub('\(.*?\)|\$|\s|,', '', selector.css("#regularprice_savings .a-color-price::text").extract()[0])
            product['original_price'] = selector.css("#price .a-text-strike::text").extract()[0].replace('$', '').replace(',', '')
            product['category_id'] = int(response.meta['category_id'])
            return product
        return None

    def parse(self, response):
        selector = Selector(response)

        # Request each product in list
        single_items = selector.css('ul.s-result-list li[id^=result_]')
        if len(single_items) > 0:
            for single_item in single_items:
                if len(single_item.xpath("@data-asin").extract()) > 0:
                    url = 'https://www.amazon.com/dp/' + single_item.xpath("@data-asin").extract()[0] + '/?psc=1'
                    yield Request(
                        url=url,
                        callback=self.single_parse,
                        headers=self.headers,
                        meta={"category_id": response.meta['category_id']}
                    )
                else:
                    print single_item.extract()

        #  Request next page if exists
        next_page = selector.css('a#pagnNextLink')
        if len(next_page.extract()) > 0:
            yield Request(
                url=response.urljoin(next_page.xpath("@href").extract()[0]),
                callback=self.parse,
                headers=self.headers, meta={"category_id": response.meta['category_id']}
            )

    def start_requests(self):
        # # execute SQL query using execute() method.
        cursor = Database.cursor()
        cursor.execute("select category_id, url from links")

        for row in cursor:
            category_id = row[0]
            url = row[1]
            yield Request(
                url=url,
                dont_filter=True,
                meta={"category_id": category_id},
                callback=self.parse,
                headers=self.headers
            )
