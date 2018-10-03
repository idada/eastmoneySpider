# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EastmoneyMasterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    titlehead = scrapy.Field()
    readcount = scrapy.Field()
    comentcount = scrapy.Field()
    author = scrapy.Field()
    pubdate = scrapy.Field()
    lastdate = scrapy.Field()
    detailid = scrapy.Field()
    code = scrapy.Field()


