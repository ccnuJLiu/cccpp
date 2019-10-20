# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector.unified import SelectorList
from module.items import ModuleItem
#上面导包路径没有问题
class SougouSpiderSpider(scrapy.Spider):
    name = 'sougou_spider_test'
    allowed_domains = ['dev.kdlapi.com']
    start_urls = ['https://dev.kdlapi.com/testproxy']

    def parse(self, response):
        # url_name = []
        temp = response.text
        print(temp)
        for i in range(10):
            yield scrapy.Request("https://dev.kdlapi.com/testproxy", callback=self.parse)



