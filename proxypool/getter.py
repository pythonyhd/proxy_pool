# -*- coding: utf-8 -*-
"""
代理获取器，配合代理爬取使用
"""
from proxypool.crawler import Crawler
from proxypool.db import RedisClient
from proxypool.settings import POOL_UPPER_THRESHOLD


class Getter(object):
    """ 代理IP获取器 """
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_limit(self):
        """ 检测是否超过代理的最大限制 """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        """ 通过python定义的元类可以顺序执行以crawl_开头的函数 """
        print("获取器开始运行，爬取免费代理")
        if not self.is_over_limit():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                # 执行获取代理的函数
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy=proxy)


if __name__ == '__main__':
    con = Getter()
    con.run()