# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 9:47
# @Author  : Yasaka.Yu
# @File    : utils.py
from retrying import retry
import requests
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent
header = {"User-Agent": UserAgent().random}


@retry(stop_max_attempt_number=8)
def downloader(url, method, data=None, options={}):
    """
    通用下载器，只处理get跟post请求
    :param url:
    :param method:
    :param data:
    :param proxies:
    :return:
    """
    headers = dict(header, **options)
    while True:
        try:
            if method == 'GET':
                response = requests.get(url=url, headers=headers, timeout=10)
                if response.status_code in [200, 201, 202]:
                    return response.text
            else:
                response = requests.post(url=url, headers=headers, data=data, timeout=10)
                if response.status_code in [200, 201, 202]:
                    return response.text
        except ConnectionError:
            print("抓取失败", url)
            return None
        except Exception as e:
            print(e.args)