# -*- coding: utf-8 -*-

from eastmoney_slave.items import EastmoneySlaveItem as emitem
import re
from w3lib.html import remove_tags
from scrapy_redis.spiders import RedisSpider
from eastmoney_slave.utils.insertredis import RedisHelper
import logging
import math
from urllib.parse import urljoin

class EmdetailSpider(RedisSpider):
    name = 'emdetailspider'
    redis_key = "slave:detail_urls"
    red = RedisHelper()
    red.ini_db()
    logger = logging.getLogger(__name__)

    def parse(self, response):
        def extract_with_xpath(content,query):
            return content.xpath(query).extract_first()

        author = extract_with_xpath(response,"//div[@id='zwconttbn']/strong/a/text()")

        #获取ID
        detailid = response.url
        detailid = re.search(r'(\d+),(\d+)', detailid)
        detailid = detailid.group(2)


        if author:  #如果是第一页
            item = emitem()
            item["content"] = extract_with_xpath(response,"//div[@class='stockcodec']/text()")
            pubtime = extract_with_xpath(response, "//div[@class='zwfbtime']/text()")
            pubtime = re.search(r' (.+) ', pubtime)
            item["pubtime"] = pubtime.group()
            item["author"] = author
            item["detailid"] = detailid
            yield item

        for tlist in response.xpath("//div[@class='zwli clearfix']"):
            #try:
            item = emitem()

            #是否含有引用
            quote = extract_with_xpath(tlist, ".//div[@class='zwlitalkbox clearfix']/text()")
            quote = remove_tags(quote) if quote else ""

            content = extract_with_xpath(tlist, ".//div[@class='zwlitext stockcodec']/text()")
            content = quote + content
            item["content"] = content
            item["author"] = extract_with_xpath(tlist, ".//span[@class='zwnick']/a/text()")
            pubtime = extract_with_xpath(tlist, ".//div[@class='zwlitime']/text()")
            pubtime = re.search(r' (.+)', pubtime)
            item["pubtime"] = pubtime.group()
            item["detailid"] = detailid
            yield item

            nextpage = response.xpath("//span[@id='newspage']/@data-page").extract_first()

            arrpage = nextpage.split("|")
            currpage = int(arrpage[-1])  # 当前页

            # 总页数，向上取整
            totalpage = math.ceil(int(arrpage[-3]) / int(arrpage[-2]))

            nextpage = arrpage[0] + str(currpage + 1) + '.html'

            # 暂时只取10页以内
            if currpage < totalpage:
                nextpage = urljoin(response.url, nextpage)
                self.red.intoredis_emdetailurl(nextpage)
                print('详细页' + nextpage + '存入redis')
            #except Exception as e:
                #self.logger.warning(e)



