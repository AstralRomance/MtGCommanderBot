import scrapy


class ScgPricesSpider(scrapy.Spider):
    name = 'scg_prices'
    allowed_domains = ['starcitygames.com']
    start_urls = ['http://starcitygames.com/']

    def parse(self, response):
        pass
