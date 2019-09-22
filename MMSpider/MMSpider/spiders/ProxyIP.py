# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from MMSpider.items import ProxyIPItem
from urllib.parse import urljoin
class ProxyipSpider(scrapy.Spider):
    name = 'ProxyIP'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/1']
    header = {

    }
    page = 1
    def parse(self, response):
        results = response.css("#ip_list >tr[class]")
        for sel in results:
            loader = ItemLoader(ProxyIPItem(),selector=sel)
            loader.add_css("ip","td:nth-of-type(2)::text")
            loader.add_css("port", "td:nth-of-type(3)::text")
            loader.add_css("Type", "td:nth-of-type(6)::text")
            loader.add_css("speed", "td:nth-of-type(7) >div::attr(title)")
            item = loader.load_item()
            if item["speed"] < 0.8 and not item["Type"].__contains__("S"):
                yield item

        _next = response.css(".next_page::attr(href)").extract_first(None)
        if _next and self.page <= 200:
            self.page += 1
            url = urljoin(response.url,_next)
            yield scrapy.Request(url)
