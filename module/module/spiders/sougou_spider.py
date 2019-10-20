# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector.unified import SelectorList
from module.items import ModuleItem
#上面导包路径没有问题
class SougouSpiderSpider(scrapy.Spider):
    name = 'sougou_spider'
    allowed_domains = ['www.sogou.com', 'snapshot.sogoucdn.com']
    start_urls = ['https://www.sogou.com/web?query=Joseph%20Paparella+linkedin&_asf=www.sogou.com']

    def parse(self, response):
        url_name = []

        for i in range(0, 6):
            temp = response.xpath("//div[@class='fb']/a[@id='sogou_snapshot_"+str(i)+"']/@href").extract()
            if not temp:
                pass
            else:
                url_name.append(temp[0])
        print("%"*2+"parse"+"%"*2)
        print(len(url_name))
        print("%" * 2 + "parse" + "%" * 2)
        for j in range(len(url_name)):
            if not url_name:
                return
            else:
                yield scrapy.Request(url_name[j], callback=self.parse_message)

    def parse_message(self, response):
        content = response.xpath("//div[@class='topcard__bottom-section']")
        image_url = content.xpath(".//img[@class='entity-image entity-image--profile entity-image--circle-8 topcard__profile-image lazy-load']/@data-delayed-url").extract()
        name_index = content.xpath(".//h1")
        if not name_index:
            name = ''
        else:
            name = name_index.xpath("string(.)").extract()[0]
        message = content.xpath(".//h2/text()").extract()
        address = content.xpath(".//h3/text()").extract()
        job = content.xpath(".//h4/text()").extract()
        right_rail = response.xpath("//div[@class='right-rail']")
        name_list = right_rail.xpath(".//img/@alt").extract()

        # image_list = right_rail.xpath(".//img/@data-delayed-url")
        item = ModuleItem(name=name, image_url=image_url, message=message, address=address, job=job)
        yield item
        right_rail = response.xpath("//div[@class='right-rail']")
        name_list = right_rail.xpath(".//img/@alt").extract()
        # print(name_list)
        for j in range(len(name_list)):
            if not name_list:
                return
            else:
                name = name_list[j]
                url = 'https://www.sogou.com/web?query=' + name + '+linkdin&_asf=www.sogou.com'
                yield scrapy.Request(url, callback=self.parse)



