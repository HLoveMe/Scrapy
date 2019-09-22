# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

connect = MySQLdb.connect(host="localhost",user="root",password="4634264015",database="SpiderBase",charset="utf8")

class MmspiderPipeline(object):
    def __init__(self):
        self.cursor = connect.cursor()

    def process_item(self, item, spider):
        sp = item.get_inset_sql()
        if sp is None:
            return item
        sql,params = sp
        self.cursor.execute(sql, params)
        connect.commit()
        return item

    def spider_closed(self, spider):
        connect.close()
