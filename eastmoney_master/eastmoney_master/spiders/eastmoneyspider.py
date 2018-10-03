# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from eastmoney_master.items import EastmoneyMasterItem as emitem
import re
from eastmoney_master.utils.insertredis import RedisHelper
from urllib.parse import urljoin
import logging
import math

class EastmoneyspiderSpider(RedisSpider):
    name = 'eastmoneyspider'
    #start_urls = ['http://eastmoney.com/']
    redis_key = "emspider:start_urls"
    red = RedisHelper()
    red.ini_db()
    logger = logging.getLogger(__name__)

    def parse(self, response):
        def extract_with_xpath(content,query):
            return content.xpath(query).extract_first()

        for tlist in response.xpath("//div[@class='articleh'] | //div[@class='articleh odd']"):
            #try:
            titlehead = extract_with_xpath(tlist,".//span/em[@class='settop']/text()")
            title = extract_with_xpath(tlist, ".//span[@class='l3']/a/text()")

            #过滤讨论或者推广，只爬取有关的信息
            if titlehead is None and title: #因为有反扒空信息，所以只取有内容的信息
                item = emitem()
                item["title"] = title
                item["titlehead"] = extract_with_xpath(tlist, ".//span[@class='l3']/em/text()")
                item["readcount"] = extract_with_xpath(tlist, ".//span[@class='l1']/text()")
                item["comentcount"] = extract_with_xpath(tlist, ".//span[@class='l2']/text()")
                item["author"] = extract_with_xpath(tlist, ".//span[@class='l4']/a/text()")
                item["pubdate"] = extract_with_xpath(tlist, ".//span[@class='l6']/text()")
                item["lastdate"] = extract_with_xpath(tlist, ".//span[@class='l5']/text()")

                detailurl = extract_with_xpath(tlist, "./span[@class='l3']/a/@href")
                arrcode = str(detailurl).split(",")
                item["detailid"] = arrcode[2].split(".")[0]
                item["code"] = arrcode[1]

                detailurl = urljoin(response.url,detailurl)
                self.red.intoredis_emdetailurl(detailurl)
                print('详细页' + detailurl + '存入redis')

                yield item
            #except Exception as e:
                #self.logger.warning(e)

        #页码信息是通过js加载，通过分析数据源得出以下规则
        nextpage = response.xpath("//span[@class='pagernums']/@data-pager").extract_first()

        arrpage = nextpage.split("|")
        currpage = int(arrpage[-1])  #当前页

        #总页数，向上取整
        totalpage = math.ceil(int(arrpage[-3]) / int(arrpage[-2]))

        nextpage = arrpage[0] + str(currpage + 1) + '.html'

        # 暂时只取10页以内
        if currpage < totalpage and currpage <= 10:
            nextpage = urljoin(response.url, nextpage)
            self.red.intoredis_emstarturl(nextpage)
            print('列表页' + nextpage + '存入redis')


