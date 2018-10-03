# python
# -*- coding: utf-8 -*-
# @File  : insertredis.py
# @Author: idada
# @Date  : 2018/9/14
# @Desc  :

import redis
from eastmoney_master.settings import REDIS_URL,PROXYCOUNT
import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, VARCHAR
import datetime

class RedisHelper():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.index_names = ('types', 'protocol', 'country', 'area', 'score')

    def ini_db(self):
        self.reds = redis.Redis.from_url(REDIS_URL, decode_responses=True)

    #股票代码集合
    def intoredis_code(self,value):
        self.intoredis_common('code',value)

    #分布式Master下载地址集合
    def intoredis_emstarturl(self,value):
        self.intoredis_common('emspider:start_urls',value)

    # 分布式slave下载地址集合
    def intoredis_emdetailurl(self, value):
        self.intoredis_common('slave:detail_urls', value)
    def intoredis_common(self,key,value):
        self.reds.sadd(key,value)

#--------------------------------------------------------------------------
    #下面为获取ip相关代码
#-------------------------------------------------------------------------
    #随机获取ip
    def getip(self):
        #json_result = json.dumps(self.select(100))
        result = self.select(PROXYCOUNT)
        return result

    def select(self,count=None, conditions=None):
        count = (count and int(count)) or 1000  # 最多返回1000条数据
        count = 1000 if count > 1000 else count

        querys = {k: v for k, v in conditions.items() if k in self.index_names} if conditions else None
        if querys:
            objects = list(self.get_keys(querys))[:count]
            redis_name = self.get_index_name('score')
            objects.sort(key=lambda x: int(self.reds.zscore(redis_name, x)))
        else:
            objects = list(
                self.reds.zrevrangebyscore(self.get_index_name("score"), '+inf', '-inf', start=0, num=count))

        result = []
        for name in objects:
            p = self.get_proxy_by_name(name)
            #result.append((p.ip, p.port, p.score))
            result.append(p.ip + ':' + p.port)
        return result

    def get_index_name(self, index_name, value=None):
        if index_name == 'score':
            return 'index::score'
        return "index::{}:{}".format(index_name, value)

    def get_keys(self, conditions):
        select_keys = {self.get_index_name(key, conditions[key]) for key in conditions.keys() if
                       key in self.index_names}
        if 'ip' in conditions and 'port' in conditions:
            return self.reds.keys(self.get_proxy_name(conditions['ip'], conditions['port'], '*'))
        if select_keys:
            return [name.decode('utf8') for name in self.reds.sinter(keys=select_keys)]
        return []

    def get_proxy_name(self, ip=None, port=None, protocal=None, proxy=None):
        ip = ip or proxy.ip
        port = port or proxy.port
        protocal = protocal or proxy.protocol
        return "proxy::{}:{}:{}".format(ip, port, protocal)

    def get_proxy_by_name(self, name):
        pd = self.reds.hgetall(name)
        if pd:
            return Proxy(**{k: v for k, v in pd.items()})

BaseModel = declarative_base()

class Proxy(BaseModel):
    __tablename__ = 'proxys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    types = Column(Integer, nullable=False)
    protocol = Column(Integer, nullable=False, default=0)
    country = Column(VARCHAR(100), nullable=False)
    area = Column(VARCHAR(100), nullable=False)
    updatetime = Column(DateTime(), default=datetime.datetime.utcnow)
    speed = Column(Numeric(5, 2), nullable=False)
    score = Column(Integer, nullable=False, default=10)

# if __name__ == '__main__':
#     rd = RedisHelper()
#     print(rd.getip())