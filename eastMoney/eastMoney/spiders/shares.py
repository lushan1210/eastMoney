# -*- coding: utf-8 -*-
import scrapy


class SharesSpider(scrapy.Spider):
    name = 'shares'
    allowed_domains = ['http://quote.eastmoney.com/sh600109.html']
    start_urls = ['http://quote.eastmoney.com/sh600109.html']

    def parse(self, response):
        price = response.css("#arrowud strong")
        a = response.text
        print(response)
        pass
