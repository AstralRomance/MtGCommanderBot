import scrapy
from scrapy.http.request import Request
from scrapy.selector import Selector
from scg_price.items import ScgPriceItem

class StarcytigamesSpider(scrapy.Spider):
    name = 'starcitygames'

    def parse(self, response):
        print('crawling')
        prices_item = ScgPriceItem()
        selector = Selector(text=response.text)
        prices = []
        for card_item in selector.xpath('//div[@class="hawk-results-item"]'):
            card_set = card_item.xpath('.//p[@class="hawk-results-item__category"]//a/text()').get()
            card_info = []
            for card_box in card_item.xpath('.//div[@class="hawk-results-item__options-table-row"]'):
                condition = card_box.xpath('.//div[@class="hawk-results-item__options-table-cell hawk-results-item__options-table-cell--name childCondition"]/text()').get().strip()[:-2]
                if condition != '':
                    price = card_box.xpath('.//div[@class="hawk-results-item__options-table-cell hawk-results-item__options-table-cell--price childAttributes"]/text()').get().strip()
                    if price != '':
                        card_info.append({condition:price})
            prices.append({card_set:card_info})
        print(prices)
        return prices
