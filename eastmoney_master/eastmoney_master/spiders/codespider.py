# python
# -*- coding: utf-8 -*-
# @File  : codespider.py
# @Author: idada
# @Date  : 2018/9/14
# @Desc  :

import scrapy
from eastmoney_master.utils.insertredis import RedisHelper
import re

class CodeSpider(scrapy.Spider):
    name = "codespider"
    start_urls = ['http://quote.eastmoney.com/stock_list.html']
    red = RedisHelper()
    red.ini_db()

    def parse(self, response):
        for codes in response.xpath("//div[@class='quotebody']").xpath(".//li"):
            #取非2打头的代码
            code = codes.xpath("a/text()").extract_first()
            code = re.search(r'\(([^2]\d+)\)', code)
            if code:
                self.red.intoredis_code(code.group(1))
                print(code.group(1) + "成功存入！")
                emurlc = code.group(1) if code.group(1)[:1] in ['6','0','3'] else 'of' + code.group(1)
                emurl = 'http://guba.eastmoney.com/list,%s.html' % emurlc
                self.red.intoredis_emstarturl(emurl)


if __name__ == "__main__":
    from scrapy import cmdline
    cmdline.execute("scrapy crawl codespider".split())




