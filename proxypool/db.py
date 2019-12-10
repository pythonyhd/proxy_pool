# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 10:47
# @Author  : Yasaka.Yu
# @File    : db.py
"""
存储器，支持redis存储，使用zset对代理去重加评分，提供flask的api接口
"""
import random
from proxypool.error import PoolEmptyError
import redis
import re
from proxypool.settings import HOST,PORT,PASSWORD,DB,INITIAL_SCORE,REDIS_KEY,MIN_SCORE,MAX_SCORE


class RedisClient(object):
    def __init__(self):
        if PASSWORD:
            self.client = redis.StrictRedis(host=HOST, port=PORT, password=PASSWORD, db=DB)
        else:
            self.client = redis.StrictRedis(host=HOST, port=PORT, db=DB)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理,score用于排序。如果该元素已经存在，则根据score更新该元素的顺序。
        :return:
        """
        if not re.match(r'\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print("代理不合法:", proxy)
            return
        if not self.client.zscore(REDIS_KEY, proxy):
            return self.client.zadd(REDIS_KEY, {proxy: score})  # python与新版本交互，传入的是mapping

    def random(self):
        """
        随机获取有效代理，首先获取分数最高的代理IP，如果不存在按照分数排序，否则抛出异常，配置文件设置最大量是100个IP
        :return:得分最高的ip
        """
        # 返回名称为key的zset中score >= min且score <= max的所有元素
        result = self.client.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
        if len(result):
            return random.choice(result)
        else:
            # 返回名称为key的zset（元素已按score从大到小排序）中的index从start到end的所有元素
            result = self.client.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise PoolEmptyError

    def decrase(self, proxy):
        """
        代理ip，score减分，每次减分，当小于最小值的时候删除，提供给检测器使用
        :return: 修改完的代理score
        """
        # 返回名称为key的zset中元素element的score
        score = self.client.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            # print("代理:{}-当前score:{}-请求不到检测的网址".format(proxy, score))
            # key, increment, member 如果在名称为key的zset中已经存在元素member，则该元素的score增加increment；否则向集合中添加该元素，其score的值为increment
            return self.client.zincrby(REDIS_KEY, -2, proxy)  # python与新版本redis交互，两个参数换过来了
        else:
            # print("代理", proxy, '分数', score, "删除")
            return self.client.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy: 代理IP
        :return:
        """
        return not self.client.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理IP
        :return: 设置的结果
        """

        # print("代理IP", proxy, "正常,设置score为:", MAX_SCORE)
        return self.client.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        获取数量
        :return:
        """
        # 返回名称为key的zset的基数
        return self.client.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.client.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.client.zrevrange(REDIS_KEY, start, stop - 1)

    def delete(self, proxy):
        """
        删除代理
        :return:
        """
        return self.client.zrem(REDIS_KEY, proxy)


if __name__ == '__main__':
    conn = RedisClient()
    # proxy = '120.83.111.70:9999'

    # res = conn.add(proxy)
    # print(res)
    result = conn.batch(0, 60)
    print(result)
    # all_proxy = conn.all()
    # print(all_proxy)
    # print(len(all_proxy))