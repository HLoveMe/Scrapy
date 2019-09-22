# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
import re
import urllib.parse as parse
from Test1.items import JobbleBlogItem
class BobboleSpider(scrapy.Spider):
    name = 'Bobbole'
    allowed_domains = ['blog.jobbole.com']

    # 最新文章
    start_urls = ['http://blog.jobbole.com/all-posts/']


    def parse(self, response):
        selector = response.selector
        list = selector.xpath("//div[@id='archive']/div[@class='post floated-thumb']")
        for one in list:
            icon = one.xpath("./div[@class='post-thumb']/a[1]/img/@src").extract_first("")
            conSelec = one.xpath("./div[@class='post-meta']")[0]
            content = conSelec.xpath("./span[@class='excerpt']/p/text()").extract_first("")

            title = conSelec.xpath("./p/a[@class='archive-title']/text()").extract_first("")
            bole_url = conSelec.xpath("./p/a[@class='archive-title']/@href").extract_first("")
            time = ""
            _times  = conSelec.xpath("./p/text()").extract()
            for _time in _times:
                if re.search(r"(\d{4,})",_time):
                    time = _time.replace('\r', '').replace('\n', '').strip()
                    break

            tag = conSelec.xpath("./p/a[2]/text()").extract_first("")
            comment = conSelec.xpath("./p/a[3]/text()").extract_first("0")
            _com = re.match(r"(\d+)",comment)
            if _com:
                comment = _com.group()

            item = JobbleBlogItem()
            item["icon"] = icon
            item["content"] = content
            item["title"] = title
            item["bole_url"] = bole_url
            item["time"] = time
            item["tag"] = tag
            item["comment"] = comment
            yield item

        # 下一页'
        print("1111")
        next_url = selector.xpath("//div[@id='archive']//div[contains(@class, 'navigation')]/a[@class='next page-numbers']/@href").extract_first(None)
        if next_url:
            url = parse.urljoin(response.url,next_url),
            print("下一页", url[0])
            yield scrapy.Request(url[0])