# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 10:38
# @Author  : Yasaka.Yu
# @File    : tester.py
"""
检测器
"""
from proxypool.db import RedisClient
import asyncio
import aiohttp
import time
import sys
import json
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.settings import TEST_URL, VALID_STATUS_CODES, BATCH_TEST_SIZE


class ValidityTester(object):
    """
    检测代理是否正常
    """
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理IP
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                # real_proxy = 'http://' + proxy
                real_proxy_data = {
                    'http:': 'http://{}'.format(proxy),
                    'https:': 'https://{}'.format(proxy),
                }
                if TEST_URL.startswith('http:'):
                    real_proxy = real_proxy_data.get('http:')
                else:
                    real_proxy = real_proxy_data.get('https:')  # aiohttp不支持检测https的代理
                print("正在测试ip:{}".format(real_proxy))
                async with session.get(url=TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)  # 检测正常，设置分数
                        results = await response.text()
                        print('代理检测正常:', json.loads(results).get('origin'))
                    else:
                        self.redis.decrase(proxy)  # 检测不正常，分数减1
                        print("响应状态码不合法:{} - ip:{}".format(response.status, proxy))
            except(ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrase(proxy)  # 抛异常减分
                print("请求不到测试地址,代理不能用:{}".format(proxy))

    def run(self):
        """
        检测主函数
        :return:
        """
        # print('测试器开始运行')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.redis.batch(start, stop)  # 代理的列表
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy=proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()  # 调用sys.stdout.flush()强制它“刷新”缓冲区，这意味着它会将缓冲区中的所有内容写入终端，即使通常它会在执行此操作之前等待
                time.sleep(5)
        except Exception as e:
            print("测试器错误:{}".format(e.args))


if __name__ == '__main__':
    conn = ValidityTester()
    conn.run()