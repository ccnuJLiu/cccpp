# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import base64
import logging
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class ModuleSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ModuleDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class UserAgentDownloadMiddleware(object):
#     USER_AGENTS = [
#         'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
#         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
#         'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100409 Firefox/3.6.3 CometBird/3.6.3',
#         'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; XH; rv:8.578.498) fr, Gecko/20121021 Camino/8.723+ (Firefox compatible)',
#         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1250.0 Iron/22.0.2150.0 Safari/537.4',
#         'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'
#     ]
#
#     def process_request(self, request, spider):
#         user_agent = random.choice(self.USER_AGENTS)
#         request.headers['User-Agent'] = user_agent

class AgentMiddleware(UserAgentMiddleware):
    """
        User-Agent中间件, 设置User-Agent
    """
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
        request.headers.setdefault('User-Agent', ua)

# 隧道服务器
tunnel_host = "tps136.kdlapi.com"
tunnel_port = "15818"

# 隧道id和密码
tid = "t17147947775063"
password = "2rdjwn8q"

logger = logging.getLogger(__name__)




class IPProxyDownloadMiddleware(object):
    # def process_request(self, request, spider):
    #     proxy = "tps136.kdlapi.com:15818"
    #     user_password = "t17147947775063:2rdjwn8q"
    #     request.meta['proxy'] = proxy
    #     b64_user_password = base64.b64encode(user_password.encode('utf-8'))
    #     request.headers['Proxy-Authorization'] = 'Basic' + b64_user_password.decode('utf-8')

    def process_request(self, request, spider):

        # proxy ="tps136.kdlapi.com:15818"
        #
        # # 隧道id和密码
        # username = "t17147947775063"
        # password = "2rdjwn8q"
        # #password="3343445"
        #
        # request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password, 'proxy': proxy}
        # # print("get ip")

        # proxy = "tps136.kdlapi.com:15818"
        # username = "t17147947775063"
        # password = "2rdjwn8q"
        # request.headers['Proxy-Authorization'] = "Basic" + base64.urlsafe_b64encode(bytes((username+":"+password), "ascii")).decode("utf-8")
        # request.meta["proxy"] = proxy
        proxy_url = 'http://%s:%s@%s:%s' % (tid, password, tunnel_host, tunnel_port)
        request.meta['proxy'] = proxy_url  # 设置代理
        logger.debug("using proxy: {}".format(request.meta['proxy']))
        # 设置代理身份认证
        # Python3 写法
        auth = "Basic %s" % (base64.b64encode(('%s:%s' % (tid, password)).encode('utf-8'))).decode('utf-8')
        # Python2 写法
        # auth = "Basic " + base64.b64encode('%s:%s' % (tid, password))
        request.headers['Proxy-Authorization'] = auth





