# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


"""
表结构为
CREATE TABLE `commentlist` (
`id` int(20) NOT NULL AUTO_INCREMENT,
`title` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
`titlehead` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
`readcount` bigint(20) NULL DEFAULT 0,
`comentcount` int(11) NULL DEFAULT 0,
`author` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
`pubdate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
`lastdate` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
`code` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
`detailid` char(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
PRIMARY KEY (`id`) 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=510111;
"""

class EastmoneyMasterPipeline(object):
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
            cur.execute("insert into commentlist(title,titlehead,readcount,comentcount,"
              "author,pubdate,lastdate,detailid,code) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                item['title'],
                item['titlehead'],
                int(item['readcount']),
                item['comentcount'],
                item['author'],
                item['pubdate'],
                item['lastdate'],
                item['detailid'],
                item['code']
              ))

        except Exception as error:
            print(error)
        else:
            self.conn.commit()

        cur.close()
        return item

    def close_spider(self,spider):
        self.conn.close()
