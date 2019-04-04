# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from twisted.enterprise import adbapi
from pymysql import cursors


class GraduationProjectPipeline(object):
    pass


class SaveOriginMessagePipeline(object):
    def __init__(self):
        # db_params = {
        #     'host': '47.107.109.117',
        #     'port': 3306,
        #     'user': 'gd',
        #     'password': 'gd@123456',
        #     'database': 'gp_economic_analysis_forecast',
        #     'charset': 'utf8',
        #     'cursorclass': cursors.DictCursor
        # }
        db_params = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'economic_analysis_forecast',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **db_params)
        self._select_sql = None
        self._insert_sql = None

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.origin_message_select_sql, (item.get('current_url')))
        repetition = cursor.fetchone()
        if not repetition:
            if item['db_symbol'] == 'origin_message':
                cursor.execute(self.origin_message_insert_sql, (
                    item.get('title'), item.get('pub_time'), item.get('pub_source'), item.get('all_content'),
                    item.get('current_url')))

    def handle_error(self, error, item, spider):
        logging.log(logging.INFO, error)
        print('=' * 20 + 'error' + '=' * 20)
        print(error)
        print('=' * 20 + 'error' + '=' * 20)

    @property
    def origin_message_insert_sql(self):
        if not self._insert_sql:
            self._insert_sql = """
            insert into gp_origin_message(id, title, pub_time, pub_source, all_content, current_url) values(null, %s, %s, %s, %s, %s)
            """
            return self._insert_sql
        return self._insert_sql

    @property
    def origin_message_select_sql(self):
        if not self._select_sql:
            self._select_sql = """
            select * from origin_message where current_url = %s
            """
            return self._select_sql
        return self._select_sql

