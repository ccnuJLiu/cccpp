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
    # name_save = []
    def start_requests(self):
        with open('./module/name_use.txt', 'r',encoding='gbk') as f:
            name_list1 = f.readlines()
            name_set1 = set(name_list1)
        with open('./module/name_use.txt', 'w',encoding='gbk') as fp:
            for name1 in name_set1:
                name1 = name1.strip("\n")
                fp.write(name1)
                fp.write('\n')
        with open('./module/name_use1.txt', 'r',encoding='gbk') as f:
            name_list2 = f.readlines()
            name_set2 = set(name_list2)
        name_search = name_set2.difference(name_set1)
        with open('./module/name_use1.txt', 'w',encoding='gbk') as fp:
            for name2 in name_search:
                name2 = name2.strip("\n")
                fp.write(name2)
                fp.write('\n')
        print(name_search)
        for name in name_search:
            name = name.strip("\n")
            for page in range(1,2):
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
        content = response.xpath("//div[@class='topcard__bottom-section'] | //div[@class='top-card-layout__card']")
        image_url = content.xpath(".//img[contains(@class, 'entity-image entity-image--profile entity-image--circle-8')]/@data-delayed-url").extract()
        name = content.xpath(".//img[contains(@class, 'entity-image entity-image--profile entity-image--circle-8')]/@alt").extract()
        # if not name_index:
        #     name = ''
        # else:
        #     name = name_index.xpath("string(.)").extract()[0]
        if not name:
            pass
        else:
            with open('./module/name_use.txt', 'a') as fp:
                name_new = name[0]
                fp.write(name_new)
                fp.write('\n')
        message = content.xpath(".//h2/text()").extract()
        address = content.xpath(".//h3/text() | .//h3/span[@class='top-card__subline-item']/text()").extract()
        job = content.xpath(".//h4/text()").extract()

        name_list = response.xpath("//div[@class='right-rail']/div/ul/li/a/img/@alt").extract()

        # name_list = right_rail.xpath(".//img/@alt").extract()
        print(name_list)
        with open('./module/name_use1.txt', 'a') as fp:
            for name1 in name_list:
                fp.write(name1)
                fp.write('\n')
        # image_list = right_rail.xpath(".//img/@data-delayed-url")
        item = ModuleItem(name=name, image_url=image_url, message=message, address=address, job=job)
        print("sb")
        yield item

# if __name__ == '__main__':
#     with open('name_use1.txt', 'r',encoding='gbk') as f:
#         name_list1 = f.readlines()
#         name_set1 = set(name_list1)
#     with open('name_use2.txt', 'r',encoding='gbk') as f:
#         name_list2 = f.readlines()
#         name_set2 = set(name_list2)
#     name_search = name_set2.difference(name_set1)
#     print(name_list1)
#     print(name_list2)
#     print(name_search)




