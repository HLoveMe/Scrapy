# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import hashlib
import w3lib

def url_md5(url):
    if isinstance(url,str):
        url = url.encode("utf8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
from scrapy.loader.processors import MapCompose,Compose,TakeFirst,Identity,Join


class JobbleBlogItem(scrapy.Item):
    icon = scrapy.Field()  #不保存
    content = scrapy.Field()
    title = scrapy.Field()
    bole_url = scrapy.Field() #不保存
    time = scrapy.Field()
    tag = scrapy.Field()
    comment = scrapy.Field()


    # 图片本地路径
    icon_path = scrapy.Field()
    #url
    # bole_url_md5 = scrapy.Field()


    def get_insert_sql(self):
        sql = """
            insert into  blog_ari(content,title,bole_url_md5,time,tag,comment,icon_path) VALUES (%s, %s, %s, %s , %s, %s, %s)
        """
        return (sql,(
            self["content"],
            self["title"],
            self["bole_url"],
            self["time"],
            self["tag"],
            self["comment"],
            self.get("icon_path", "")
        ))
