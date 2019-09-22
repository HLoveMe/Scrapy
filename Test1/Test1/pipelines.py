# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class Test1Pipeline(object):
    def process_item(self, item, spider):
        return item



"""
    保存到Json
"""
from scrapy.exporters import JsonLinesItemExporter
class JsonPickerPipe(object):
    def __init__(self):
        self.jsonfile = open("arts.json","wb")
        self.exporter = JsonLinesItemExporter(self.jsonfile,encoding="utf-8")
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.jsonfile.close()
        self.exporter.finish_exporting()

"""
    下载图片
"""
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
class BolggleImagePipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
        icon = item['icon']
        if len(icon) >= 5:
            yield scrapy.Request(icon)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['icon_path'] = image_paths.pop()
        return item


"""
    保存到数据库
"""
import MySQLdb
class MYSQLPipelines(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost",user="root",password="4634264015",database="BloggBase",charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql,paras = item.get_insert_sql()
        self.cursor.execute(sql,paras)
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()

    # @classmethod
    # def from_crawler(cls, crawl):
    #     pass

