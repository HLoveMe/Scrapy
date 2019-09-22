# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


import MySQLdb
connect = MySQLdb.connect(host="localhost",user="root",password="4634264015",database="SpiderBase",charset="utf8")
import random

"""
    User_Agent
"""
from fake_useragent import UserAgent

class MmSpiderDownLoaderUserAgent(object):
    def __init__(self):
        self.ua = UserAgent()
        pass

    def process_request(self, request, spider):
        request.headers["User-Agent"] = self.ua.random
        pass

"""
    代理IP
"""
class MmspiderDownloaderProxyMiddleware(object):

    def __init__(self):
        self.cursor = connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if request.url.__contains__("xicidaili"):
            return None
        sql = """
            select ip,port,Type from ProxyInfo order by rand() LIMIT 0,1
        """
        # self.cursor.execute(sql)
        # data = self.cursor.fetchone()
        # request.meta["proxy"] = "http://{0}:{1}".format(data[0],data[1])
        #121.232.146.39:9000
        # request.meta["proxy"] = "http://121.225.24.219:3128"
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
