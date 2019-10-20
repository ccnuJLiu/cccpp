#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 16:26
# @Author  : Lelsey
# @Site    : 
# @File    : start.py.py
# @Software: PyCharm


from scrapy import cmdline

cmdline.execute("scrapy crawl sougou_spider".split())
