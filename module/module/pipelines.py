# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

import scrapy
from scrapy.exporters import JsonLinesItemExporter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class ModulePipeline(object):
    # def __init__(self):
    #     self.fp = open("sogou.json",'wb')
    #     self.exporter = JsonLinesItemExporter(self.fp ,ensure_ascii=False,encoding='utf-8')

        # self.exporter.start_exporting()
    def open_spider(self,spider):
        print("start!!")
    def process_item(self, item, spider):
        if item['name']:
            client = MongoClient("mongodb://127.0.0.1:27017")
            db = client.LinkedinData
            DataSet = db.DataSet
            DataSet.insert({"name":item["name"],
                            "image_url":item["image_url"],
                            "message":item["message"],
                            "address":item["address"],
                            "job":item["job"],
                            "name_url":item["name_url"],
                            "image_name":item["image_name"]})
            # self.exporter.export_item(item)
        else:
            pass
        return item
    def close_spider(self,spider):
        # self.exporter.finish_exporting()
        # self.fp.close()
        print("end!!")

class DownLoadPipeline(ImagesPipeline):

    #发生图片下载请求
    def get_media_requests(self, item, info):
        # if item['image_url'] :
        yield scrapy.Request(url=item['image_url'], meta={'item':item})


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_name = item['image_name']
        #设置图片的路径
        #下载下来的图片名字就是这个图片页面的标题加这个图片的url最后一个'/'后面内容，因为这里每个图片的title不同，也可以直接写path = item['title']
        path = image_name+".jpg"
        return path