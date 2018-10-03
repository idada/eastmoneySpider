# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

"""
以下为mysql表结构
CREATE TABLE `commentdetail` (
`id` int(20) NOT NULL AUTO_INCREMENT,
`content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
`pubtime` datetime NULL DEFAULT NULL,
`author` char(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
`detailid` char(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
PRIMARY KEY (`id`) 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=56;
"""

class EastmoneySlavePipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def __init__(self, host, user, pwd, dbname):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.dbname = dbname

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            user = crawler.settings.get('MYSQL_USER'),
            pwd = crawler.settings.get('MYSQL_PASSWD'),
            dbname = crawler.settings.get('MYSQL_DBNAME')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host, user=self.user,
                                    password=self.pwd, db=self.dbname, charset='utf8')

    def process_item(self, item, spider):
        cur = self.conn.cursor()
        try:
            cur.execute("insert into commentdetail(content,pubtime,author,detailid)"
              " values(%s,%s,%s,%s)",(
                item['content'],
                item['pubtime'],
                item['author'],
                item['detailid']
              ))

        except Exception as error:
            print(error)
        else:
            self.conn.commit()

        cur.close()
        return item

    def close_spider(self,spider):
        self.conn.close()