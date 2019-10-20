# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exporters import JsonLinesItemExporter
class ModulePipeline(object):
    def __init__(self):
        self.fp = open("sogou.json",'wb')
        self.exporter = JsonLinesItemExporter(self.fp ,ensure_ascii=False,encoding='utf-8')
        # self.exporter.start_exporting()
    def open_spider(self,spider):
        print("start!!")
    def process_item(self, item, spider):
        if item['name']:
            self.exporter.export_item(item)
        else:
            pass
        return item
    def close_spider(self,spider):
        # self.exporter.finish_exporting()
        self.fp.close()
        print("end!!")