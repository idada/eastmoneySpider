# python
# -*- coding: utf-8 -*-
# @File  : txt.py
# @Author: idada
# @Date  : 2018/9/20
# @Desc  :

content = """
<a data-page="1" href="list,000028_1.html" target="_self">首页</a>
<a data-page="1" class="on" href="list,000028_1.html" target="_self">1</a>
<a data-page="2" href="list,000028_2.html" target="_self">2</a>
<a data-page="3" href="list,000028_3.html" target="_self">3</a>
<a data-page="4" href="list,000028_4.html" target="_self">4</a>
<a data-page="5" href="list,000028_5.html" target="_self">5</a>
<a data-page="6" href="list,000028_6.html" target="_self">6</a>
<a data-page="7" href="list,000028_7.html" target="_self">7</a>
<a data-page="8" href="list,000028_8.html" target="_self">8</a>
<a data-page="9" href="list,000028_9.html" target="_self">9</a>
<a data-page="10" href="list,000028_10.html" target="_self">10</a>
<a data-page="11" href="list,000028_11.html" target="_self">11</a>
<a data-page="2" href="list,000028_2.html" target="_self">下一页</a>
<a data-page="232" href="list,000028_232.html" target="_self">尾页</a>
<span class="sumpage">232</span>
"""
import re

cc = re.search(r'href="(.+?)" target="_self">下一页</a>',content)
if cc:
    print(cc.group(1))

url = 'http://guba.eastmoney.com/list,000028.html'
from urllib.parse import urljoin
print(urljoin(url,"list,000028_2.html"))

content = 'list,000028_10.html'
cc = re.search(r'_(\d+)',content).group(1)

print(cc)