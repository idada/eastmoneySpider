# eastmoneySipder

1.基于scrapy-redis分布式，采集东方财富网股吧内容

2.运行环境：python3.6，redis,mysql

3.所有的python包可通过Anaconda导入emspider.yaml
文件

使用说明

1.分成三个项目

2.ip代理池用的是七夜的自动更新ip

3.首先运行eastmoney_master\spiders下的codespider，获取种子网址

4.在命令行下运行scrapy crawl eastmoneyspider,会采集股吧列表信息，加入到redis里并把相关信息存储到mysql

5.详细内容通过分机运行eastmoney_slave\spiders下的emdetailspider爬虫

6.因为数据量太大，当前只爬取了列表页前10页内容，可通过修改代码确定自己要爬多少，一页80条数据，大概有4800个股票代码，
有些股票有几百页，一条评论的详细页可能含有上百条的评论，所以总数据量吓人

7.去重采用的redis的set集合简单去重


待完善之处

1.通过分析地址信息，发现很多就是后半部分的股票代码不同，所以一大部分是冗余信息，这样可通过地址拼接只保存一些关键数据
2.暂时没有试过大概数据达到多少redis会出现内存溢出

3.警报机制
