# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.selector.unified import SelectorList
from module.items import ModuleItem
#上面导包路径没有问题
class SougouSpiderSpider(scrapy.Spider):
    name = 'sougou_spider_cp'
    allowed_domains = ['www.sogou.com', 'snapshot.sogoucdn.com']
    # start_urls = ['https://www.sogou.com/web?query=Joseph%20Paparella+linkedin&_asf=www.sogou.com']
    url_template = 'https://www.sogou.com/web?query={name}+linkedin&_asf=www.sogou.com&page={page}'
    # name_save = []
    def start_requests(self):
        client = MongoClient('localhost', 27017)
        db = client.LinkedinData
        oldDataSet = db.oldName
        newDataSet = db.newName
        dict_old = oldDataSet.find()
        name_old = set()
        dict_new = newDataSet.find()
        name_new = set()
        for dict_name1 in dict_old:
            name_old.add(dict_name1["name"])

        for dict_name2 in dict_new:
            name_new.add(dict_name2["name"])

        oldDataSet.delete_many({})
        newDataSet.delete_many({})
        for name1 in name_old:
            oldDataSet.insert({"name":name1})
        name_search = name_new.difference(name_old)
        for name2 in name_search:
            newDataSet.insert({"name":name2})
        name_search = name_new.difference(name_old)
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

        for j in range(len(url_name)):
            if  not url_name:
                return
            else:
                yield scrapy.Request(url_name[j], callback=self.parse_message)

    def parse_message(self, response):
        # client = MongoClient("mongodb://127.0.0.1:27017")
        # db = client.LinkedinData
        content = response.xpath("//div[@class='topcard__bottom-section'] | //div[@class='top-card-layout__card']")
        image_url = content.xpath(".//img[contains(@class, 'entity-image entity-image--profile entity-image--circle-8')]/@data-delayed-url").extract()

        if not image_url:
            image_name =""
        else:
            image_url = image_url[0]
            image_hashcode = hash(image_url)
            if image_hashcode < 0:
                image_name = str(abs(image_hashcode))+"-"
            else:
                image_name = str(image_hashcode)
        name = content.xpath(".//img[contains(@class, 'entity-image entity-image--profile entity-image--circle-8')]/@alt").extract()
        if not name:
            pass
        else:
            name_old = name[0]
            client = MongoClient("mongodb://127.0.0.1:27017")
            db = client.LinkedinData
            oldDataSet = db.oldName
            oldDataSet.insert({"name":name_old})
        message = content.xpath(".//h2/text()").extract()
        address = content.xpath(".//h3/text() | .//h3/span[@class='top-card__subline-item']/text()").extract()
        job = content.xpath(".//h4/text()").extract()
        name_url = content.xpath("/html/body/div[1]/div/p/a/@href").extract()
        name_list = response.xpath("//div[@class='right-rail']/div/ul/li/a/img/@alt").extract()
        job_experience_index  = response.xpath("//section[@class='experience pp-section']/ul")
        job_experience  = job_experience_index.xpath("string(.)").extract()
        study_experience_index  = response.xpath("//section[@class='education pp-section']/ul")
        study_experience  = study_experience_index.xpath("string(.)").extract()

        for name1 in name_list:
            client = MongoClient("mongodb://127.0.0.1:27017")
            db = client.LinkedinData
            newDataSet = db.newName
            newDataSet.insert({"name":name1})
        if name and image_url:
            if "https://static-exp" in image_url:
                pass
            else:
                item = ModuleItem(name=name, image_url=image_url, message=message, address=address, job=job,name_url=name_url,image_name=image_name,job_experience=job_experience,study_experience=study_experience)
                yield item
        else:
            pass
