# python
# -*- coding: utf-8 -*-
# @File  : sipder.py
# @Author: idada
# @Date  : 2018/9/21
# @Desc  :

import scrapy
import re
from eastmoney_master.utils.insertredis import RedisHelper
from urllib.parse import urljoin
import logging
import math

class SpiderTxt(scrapy.Spider):
    name = "SpiderTxt"
    start_urls = ['http://guba.eastmoney.com/list,000028.html']

    def parse(self, response):
        def extract_with_xpath(content,query):
            return content.xpath(query).extract_first()
        for tlist in response.xpath("//div[@class='articleh'] | //div[@class='articleh odd']"):
            titlehead = extract_with_xpath(tlist, ".//span/em[@class='settop']/text()")
            title = extract_with_xpath(tlist, ".//span[@class='l3']/a/text()")

            if titlehead is None and title:

                detailurl = extract_with_xpath(tlist, "./span[@class='l3']/a/@href")

                arrcode = str(detailurl).split(",")
                print(detailurl)
                print(len(arrcode))
                print(extract_with_xpath(tlist, ".//span[@class='l3']/a/text()"))
                # print(arrcode[2])
                # print(arrcode[1])

                detailurl = urljoin(response.url, detailurl)

                #print(detailurl)

        nextpage = response.xpath("//span[@class='pagernums']/@data-pager").extract_first()

        arrpage = nextpage.split("|")
        currpage = arrpage[-1]
        totalpage = math.ceil(int(arrpage[-3]) / int(arrpage[-2]))
        print(totalpage)

        #nextpage = re.search(r'href="(.+?)" target="_self">下一页</a>',nextpage)
        #print(nextpage)
        # if nextpage:
        #     nextpage = nextpage.group(1)
        #     #------------------------------------------
        #     #暂时只取10页以内
        #     pagenum = re.search(r'_(\d+)',nextpage)
        #     if pagenum:
        #         if int(pagenum)<10:
        #             ##---------------  end  --------------------
        #             nextpage = urljoin(response.url, nextpage)
        #             #self.red.intoredis_emstarturl(nextpage)
        #             print('列表页' + nextpage + '存入redis')

if __name__ == "__main__":
    from scrapy import cmdline
    cmdline.execute("scrapy crawl SpiderTxt".split())