from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from amazon.spiders.single import SingleSpider

process = CrawlerProcess(get_project_settings())

process.crawl(SingleSpider)
process.start()
