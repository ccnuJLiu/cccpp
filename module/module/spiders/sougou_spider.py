# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector.unified import SelectorList
from module.items import ModuleItem
#上面导包路径没有问题
class SougouSpiderSpider(scrapy.Spider):
    name = 'sougou_spider'
    allowed_domains = ['www.sogou.com', 'snapshot.sogoucdn.com']
    # start_urls = ['https://www.sogou.com/web?query=Joseph%20Paparella+linkedin&_asf=www.sogou.com']
    url_template = 'https://www.sogou.com/web?query={name}+linkedin&_asf=www.sogou.com&page={page}'
    name_save = []
    def start_requests(self):
        with open('./module/spiders/name_use.txt', 'r') as f:
            name_list = f.readlines()
        for name in name_list:
            name = name.strip("\n")
            for page in range(1, 4):
                url_next = self.url_template.format(name=name,page=page)
                yield scrapy.Request(url_next,callback=self.parse)

    def parse(self, response):
        url_name = []
        for i in range(0,8):
            temp1 = response.xpath("//div[@class='fb']/a[@id='sogou_snapshot_"+str(i)+"']/@href").extract()
            temp2 = response.xpath("//div[@class='fb']/cite[@id='cacheresult_info_" + str(i)+"']/text()").extract()
            if not temp1 :
                pass
            else:
                if not temp2:
                    pass
                else:
                    if "linkedin.com" in temp2[0] :
                        url_name.append(temp1[0])

        print("%"*2+"parse"+"%"*2)
        print(url_name)
        print("%" * 2 + "parse" + "%" * 2)
        for j in range(len(url_name)):
            if  not url_name:
                return
            else:
                yield scrapy.Request(url_name[j], callback=self.parse_message,dont_filter=True)

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
        right_rail = response.xpath("//div[contains(@class,'right-rail')]")
        name_list = right_rail.xpath(".//img/@alt").extract()
        try:
            fp = open("./module/spiders/name_use.txt","a")
            for name in name_list:
                if name.encode('UTF-8').isalpha() and not "inkedin" in name:
                    self.name_save.append(name)
                    fp.write(name)
                    fp.write('\n')
        finally:
            fp.close()
        # image_list = right_rail.xpath(".//img/@data-delayed-url")
        item = ModuleItem(name=name, image_url=image_url, message=message, address=address, job=job)
        yield item
        # right_rail = response.xpath("//div[@class='right-rail']")
        # name_list = right_rail.xpath(".//img/@alt").extract()
        # # print(name_list)
        # for j in range(len(name_list)):
        #     if not name_list:
        #         return
        #     else:
        #         name = name_list[j]
        #         url = 'https://www.sogou.com/web?query=' + name + '+linkdin&_asf=www.sogou.com'
        #         yield scrapy.Request(url, callback=self.parse)


