# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ModuleItem(scrapy.Item):
    name = scrapy.Field()
    image_url = scrapy.Field()
    message = scrapy.Field()
    address = scrapy.Field()
    job = scrapy.Field()
    # name_url = scrapy.Field()

