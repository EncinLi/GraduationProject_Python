# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class GraduationProjectPipeline(object):
    pass


class SaveDataInMySqlPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '47.107.109.117',
            'port': 3306,
            'user': 'gd',
            'password': 'gd@123456',
            'database': '',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, ())

    def handle_error(self, error, item, spider):
        print('=' * 20 + 'error' + '=' * 20)
        print(error)
        print('=' * 20 + 'error' + '=' * 20)

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into 
            """
            return self._sql
        return self._sql
