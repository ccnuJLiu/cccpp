# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SogouspiderUpSpider(CrawlSpider):
    name = 'sogouspider_up'
    allowed_domains = ['www.sogou.com']
    start_urls = ['https://www.sogou.com/web?query=wang+linkedin']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.sogou.com/web?query='), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
