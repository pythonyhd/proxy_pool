# -*- coding: utf-8 -*-
from retrying import retry
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout
from fake_useragent import UserAgent

header = {"User-Agent": UserAgent().random}


def downloader(url, method, data=None, headers={}, proxies=None, retry_times=10):
    """
    通用下载器
    :param url: url
    :param method: 请求方法，只支持get跟post
    :param data: post表单参数
    :param proxies: 代理
    :param retry_times: 重试次数
    :return: 响应结果
    """
    headers = dict(header, **headers)
    while retry_times > 0:
        try:
            if method == 'GET':
                if proxies:
                    res = requests.get(url=url, headers=headers, proxies=proxies, timeout=30)
                else:
                    res = requests.get(url=url, headers=headers, timeout=30)
            else:
                if proxies:
                    res = requests.post(url=url, data=data, headers=headers, proxies=proxies, timeout=30)
                else:
                    res = requests.post(url=url, data=data, headers=headers, timeout=30)
            if res.status_code in [200, 201, 202]:
                return res.text
        except (ConnectTimeout, ReadTimeout, ConnectionError):
            print("抓取失败", url)
            return None
        except Exception as e:
            print(f'请求出错:{repr(e)}--开始重试')
            if retry_times > 0:
                retry_times -= 1


@retry(stop_max_attempt_number=8)
def downloader_old(url, method, data=None, options={}):
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
        except (ConnectTimeout, ReadTimeout, ConnectionError):
            print("抓取失败", url)
            return None
        except Exception as e:
            print(e.args)