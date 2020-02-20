# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors

from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class FirstSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JSONWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('pachong.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 使用scrapy提供的jsonExporter导出json文件
    def __init__(self):
        self.file = open("pa_exporter.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class MysqlPipeline(object):
    # 将数据保存到mysql数据库中
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '', 'first', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into home(head_image_url, title, photoNum, url_object_id)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["head_image_url"], item["title"], item["photoNum"], item["url_object_id"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    # 异步操作操作数据库
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            passwd = settings["MYSQL_PASSWORD"],
            user = settings["MYSQL_USER"],
            charset = "utf8",
            use_unicode = True,
            cursorclass = MySQLdb.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
                    insert into home(head_image_url, title, photoNum, url_object_id)
                    VALUES (%s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["head_image_url"], item["title"], item["photoNum"], item["url_object_id"]))


class FirstSpiderImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "head_image_url" in item:
            for ok, values in results:
                head_image_path = values['path']
            item["head_image_path"] = head_image_path
            return item
