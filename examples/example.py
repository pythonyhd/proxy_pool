# -*- coding: utf-8 -*-
import random
import time

import redis
import requests
from fake_useragent import UserAgent
from lxml import etree

# redis连接池
pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=15)
# 从池子里面取除值
redis_client = redis.Redis(connection_pool=pool, decode_responses=True)
REDIS_KEY = "freeproxies"


def get_proxy_from_redis():
    proxy_list = redis_client.zrevrange(REDIS_KEY, 0, 61)
    proxy = random.choice(proxy_list)
    proxies = {
        'http': 'http://{}'.format(proxy.decode('utf-8')),
        'https': 'https://{}'.format(proxy.decode('utf-8')),
    }

    return proxies


def crawler():
    headers = {
        'User-Agent': UserAgent().random,
    }
    url = 'https://www.ubaike.cn/show_10672628.html'
    for _ in range(1, 61):
        proxies = get_proxy_from_redis()
        print("当前ip:{}".format(proxies))
        res = requests.get(url=url, headers=headers, proxies=proxies, timeout=15)
        doc = etree.HTML(res.text)
        title = doc.xpath('//h1[@class="title"]/text()')
        print("企业名称:{}".format(title))


def statistic_time(function):
    def wrapper(*args, **kwargs):
        print('[Function {name} start]'.format(name=function.__name__))
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        print('[Function: {name} finished spent time:{time:.2f}s]'.format(name=function.__name__, time=end_time-start_time))
        return result
    return wrapper


if __name__ == '__main__':
    conn = crawler()