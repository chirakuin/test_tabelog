# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import os
from contextlib import closing

from scrapy.exceptions import DropItem

class ValidationPipeline:

    def process_item(self, item, spider):
        if not item['body']:
            raise DropItem('Missing body')

        return item


class SqLitePipeline:

    def open_spider(self, spider):
        setting = spider.settings

        db_name = os.path.join(os.getcwd(), 'tabelog_02.db')

        # db = '/Users/cc/Documents/crawler/scrapy_01/testproject/testproject/tebelog_db'
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

        create_table = '''create table if not exists users (id_key INTEGER PRIMARY KEY, name varchar(32), url varchar(64),body text)'''
        self.c.execute(create_table)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        sql = 'insert into users (name, url, body) values (?,?,?)'
        users = (item['name'],item['url'], item['body'])
        self.c.execute(sql, users)
        self.conn.commit()

        create_sql = 'create table table_1 as select name, url, body from users group by body'
        self.c.execute(create_sql)
        # self.conn.commit()

        drop_sql = 'drop table users'
        self.c.execute(drop_sql)
        # self.conn.commit()

        rename_sql = 'alter table table_1 rename to users'
        self.c.execute(rename_sql)
        self.conn.commit()

        return item

        select_sql = 'select * from users'
        for row in self.c.execute(select_sql):
            print(row)



    #     create_table = '''create table if not exists users (id_key INTEGER PRIMARY KEY, name varchar(32), url varchar(64),
    #                     user varchar(32), attr varchar(32), star_dinner varchar(32), star_lunch varchar(32), 
    #                     price_dinner varchar(32), price_lunch varchar(32), times varchar(32), day  varchar(32), title varchar(64), body text)'''
    #     self.c.execute(create_table)
    #     self.conn.commit()

    # def close_spider(self, spider):
    #     self.conn.close()

    # def process_item(self, item, spider):
    #     sql = 'insert into users (name, url, user, attr, star_dinner, star_lunch, price_dinner, price_lunch, times, day, title, body) values (?,?,?,?,?,?,?,?,?,?,?,?)'
    #     users = (item['name'],item['url'], item['user'], item['attr'], item['star_dinner'], item['star_lunch'], 
    #             item['price_dinner'], item['price_lunch'], item['times'], item['day'], item['title'], item['body'])
    #     self.c.execute(sql, users)
    #     self.conn.commit()

    #     create_sql = 'create table table_1 as select name, url, user, attr, star_dinner, star_lunch, price_dinner, price_lunch, times, day, title, body from users group by title'
    #     self.c.execute(create_sql)
    #     # self.conn.commit()

    #     drop_sql = 'drop table users'
    #     self.c.execute(drop_sql)
    #     # self.conn.commit()

    #     rename_sql = 'alter table table_1 rename to users'
    #     self.c.execute(rename_sql)
    #     self.conn.commit()

    #     return item

    #     select_sql = 'select * from users'
    #     for row in self.c.execute(select_sql):
    #         print(row)