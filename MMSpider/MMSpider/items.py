# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,Compose,TakeFirst,Identity,Join
import re
class MmspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def filter_speed(value):
    res = re.match(r"([\d\\.]{4})",value)
    if res:
        return float(res.group(1))
    return 100

class ProxyIPItem(scrapy.Item):
    ip = scrapy.Field(
        output_processor=TakeFirst()
    )
    port = scrapy.Field(
        output_processor=TakeFirst()
    )
    Type = scrapy.Field(
        output_processor=TakeFirst()
    )
    speed= scrapy.Field(
        output_processor=TakeFirst(),
        input_processor = MapCompose(filter_speed)
    )
    def get_inset_sql(self):
        sql = """
            insert into ProxyInfo(ip,port,Type) VALUES (%s,%s,%s)
        """
        print(type(self["speed"]))
        params = (self["ip"],self["port"],self["Type"])
        return (sql,params)
    pass


class MM176TypeItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

    def get_inset_sql(self):
        sql = """
            insert into MM176Type(name,url) VALUES (%s,%s)
        """
        params = (self["name"],self["url"])
        return (sql,params)


class MM176PersonItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    href = scrapy.Field(
        output_processor=TakeFirst()
    )
    tags = scrapy.Field(
        output_processor=Join("-")
    )

    id = scrapy.Field(
        output_processor=TakeFirst()
    )
    next = scrapy.Field(
        output_processor=TakeFirst()
    )

    def get_inset_sql(self):
        try:
            if len(self["next"]) <= 10:
                # last
                sql = """
                        insert into MMItem(title,id,tags) VALUES (%s,%s,%s)
                    """
                params = (self["title"], self["id"], self["tags"])
            else:
                sql = """
                        insert into MMItem(href,id) VALUES (%s,%s)
                """
                params = (self["href"], self["id"])
            return (sql, params)
        except :
            # last
            sql = """
                               insert into MMItem(title,id,tags) VALUES (%s,%s,%s)
                            """
            params = (self["title"], self["id"], self["tags"])
            return (sql, params)
            pass
