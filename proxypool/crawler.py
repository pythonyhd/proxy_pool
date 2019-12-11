# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 17:56
# @Author  : Yasaka.Yu
# @File    : crawler.py
"""
IP代理下载器
"""
import logging
from proxypool.utils import downloader
from pyquery import PyQuery as pq
import re
from lxml import etree
import execjs
import base64
import os
logger = logging.getLogger(__name__)
TEMPLATES_PATH = os.path.dirname(os.path.dirname(__file__)) + r'/templates/decodeip.js'
BAIBIAN_PATH = os.path.dirname(os.path.dirname(__file__)) + r'/templates/baibian.js'


class ProxyMetaclass(type):
    """
    代理IP抓取元类，
    检测所有的方法名，如果方法名以crawl开头，重新赋值加到列表里面，可以传递方法名执行函数
    在Crawler类中加入__CrawlFunc__和__CrawlFuncCount__两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    """
    抓取各大免费网站的代理IP，可以自由添加，函数名必须以crawl开头
    """
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            proxies.append(proxy)
            logger.debug("代理获取成功- {} -".format(proxy))
        return proxies

    @classmethod
    def run_decode_js(cls, text):
        """
        sunjs代理JS解密
        :param text: 密文
        :return: 解密后的IP
        """
        with open(TEMPLATES_PATH, 'r', encoding='utf-8') as f:
            source_js = f.read()
            js_parttern = execjs.compile(source_js)
            result = js_parttern.call('decode', text)
            return result

    @classmethod
    def baibian_js(cls, text):
        """
        百变代理JS解密
        :param text: 密文
        :return: 解密后的IP
        """
        with open(BAIBIAN_PATH, 'r', encoding='utf-8') as f:
            js_parttern = execjs.compile(f.read())
            result = js_parttern.call('ddip', text)
            return result

    def crawl_daili66(self, page_count=4):
        """
        代理66：http://www.66ip.cn/index.html
        封IP，少量几页
        :return:
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count)]
        for url in urls:
            html = downloader(url=url, method='GET')
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()  # gt是大于,lt是小于,pyquery中第一个是从0开始
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text().strip()
                    port = tr.find('td:nth-child(2)').text().strip()
                    data = ":".join([ip, port])
                    # print("代理:{}".format(data))
                    yield data

    def crawl_ip3366(self, page_count=6):
        """
        云代理爬虫：http://www.ip3366.net/free/?stype=1
        :return:
        """
        start_url = 'http://www.ip3366.net/free/?stype=1&page={}'
        urls = [start_url.format(url) for url in range(1, page_count)]
        for url in urls:
            html = downloader(url=url, method='GET')
            if html:
                doc = pq(html)
                trs = doc('#list table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text().strip()
                    port = tr.find('td:nth-child(2)').text().strip()
                    result = ":".join([ip, port])
                    yield result

    def crawl_kuai(self):
        """
        快代理：https://www.kuaidaili.com/free/inha/1/
        :param page_count:
        :return:
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        for page in range(1, 4):
            html = downloader(url=start_url.format(page), method='GET')
            if html:
                ip_pattern = re.compile(r'<td data-title="IP">(.*?)</td>')
                port_pattern = re.compile(r'<td data-title="PORT">(\d+)</td>')
                ip_list = ip_pattern.findall(html)
                port_list = port_pattern.findall(html)
                for ip, port in zip(ip_list, port_list):
                    result = ip.strip() + ':' + port.strip()
                    yield result

    def crawl_haidaili(self):
        """
        IP海：http://www.iphai.com/
        :return:
        """
        start_url = 'http://www.iphai.com/'
        html = downloader(url=start_url, method='GET')
        doc = pq(html)
        trs = doc('.table-responsive table tr:gt(0)').items()
        for tr in trs:
            ip = tr.find('td:nth-child(1)').text().strip()
            port = tr.find('td:nth-child(2)').text().strip()
            result = ":".join([ip, port])
            yield result

    def crawl_wuyou(self):
        """
        无忧代理：http://www.data5u.com/
        :return:可用率极低
        """
        start_url = 'http://www.data5u.com/'
        html = downloader(url=start_url, method='GET')
        if html:
            ip_port_pattern = re.compile(r'<li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class="port.*?">(\d+)</li>', re.S)
            ip_port_list = ip_port_pattern.findall(html)  # 列表里面是元组
            for ip, port in ip_port_list:
                result = ":".join([ip.strip(), port.strip()])
                # print(result)
                yield result

    def crawl_kaixin(self):
        """
        开心代理：http://www.kxdaili.com/dailiip.html
        :return:
        """
        start_url = 'http://www.kxdaili.com/dailiip/1/{}.html'
        for page in range(1, 4):
            html = downloader(url=start_url.format(page), method='GET')
            if html:
                doc = pq(html)
                trs = doc('.active tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text().strip()
                    port = tr.find('td:nth-child(2)').text().strip()
                    result = ':'.join([ip, port])
                    # print(result)
                    yield result

    def crawl_free(self):
        """
        免费代理库：http://ip.jiangxianli.com/
        :return:
        """
        start_url = 'http://ip.jiangxianli.com/?page={}'
        urls = [start_url.format(page) for page in range(1, 4)]
        for url in urls:
            html = downloader(url=url, method='GET')
            if html:
                doc = pq(html)
                trs = doc('.table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text().strip()
                    port = tr.find('td:nth-child(3)').text().strip()
                    result = ":".join([ip, port])
                    # print(result)
                    yield result

    def crawl_proxylist(self):
        """
        老外：https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
        :return:
        """
        start_url = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1'
        html = downloader(url=start_url, method="GET")
        if html:
            ip_port_parteners = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>\s*<td>(\d+)</td>')
            ip_port_list = ip_port_parteners.findall(html)
            for ip, port in ip_port_list:
                result = ":".join([ip.strip(), port.strip()])
                # print(result)
                yield result

    def crawl_89ip(self):
        """
        89IP代理：http://www.89ip.cn/
        """
        start_url = 'http://www.89ip.cn/index_{}.html'
        for page in range(1, 6):
            if page == 1:
                url = 'http://www.89ip.cn/'
            else:
                url = start_url.format(page)
            html = downloader(url=url, method='GET')
            if html:
                doc = pq(html)
                trs = doc('.layui-table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text().strip()
                    port = tr.find('td:nth-child(2)').text().strip()
                    result = ":".join([ip, port])
                    # print(result)
                    yield result

    def crawl_xiaohuan(self):
        """
        小幻代理：https://ip.ihuan.me/
        :return:
        """
        start_url = 'https://ip.ihuan.me/'
        html = downloader(url=start_url, method='GET')
        if html:
            doc = pq(html)
            trs = doc('.table tbody tr').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1) a').text().strip()
                port = tr.find('td:nth-child(2)').text().strip()
                result = ":".join([ip, port])
                # print(result)
                yield result

    def crawl_xila(self):
        """
        西拉代理：http://www.xiladaili.com/gaoni/2/
        :return:
        """
        start_url = 'http://www.xiladaili.com/gaoni/{}/'
        for page in range(1, 6):
            html = downloader(url=start_url.format(page), method="GET")
            if html:
                doc = pq(html)
                trs = doc('.fl-table tbody tr').items()
                for tr in trs:
                    ip_port = tr.find('td:nth-child(1)').text().strip()
                    # print(ip_port)
                    yield ip_port
                    
    def crawl_nima(self):
        """
        尼玛代理：http://www.nimadaili.com/putong/
        :return:
        """
        start_url = 'http://www.nimadaili.com/putong/{}/'
        urls = [start_url.format(page) for page in range(1, 6)]
        ip_port_pattern = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+\:\d+)</td>')
        for url in urls:
            html = downloader(url=url, method='GET')
            if html:
                ip_port_list = ip_port_pattern.findall(html)
                for result in ip_port_list:
                    # print(result)
                    yield result

    def crawl_sunjs(self):
        """
        sunjs代理：https://www.sunjs.com/proxy/list.html
        :return:
        """
        start_url = 'https://www.sunjs.com/proxy/list.html'
        ip_list = []
        html = downloader(url=start_url, method='GET')
        selector = etree.HTML(html)
        decode_pattern = re.compile(r'decode\(\"(.*?)\"\)')
        decode_data_list = decode_pattern.findall(html, re.S)
        port_list = selector.xpath('//td[@data-title="PORT"]/text()')
        for data in decode_data_list:
            first_decode = self.run_decode_js(data)
            ip_bytes = base64.b64decode(first_decode)
            ip = str(ip_bytes, encoding='utf-8')
            ip_list.append(ip)

        for ip, port in zip(ip_list, port_list):
            results = ip + ':' + port
            # print(results)
            yield results

    def crawl_baibian(self):
        """
        百变IP：https://www.baibianip.com/home/free.html
        :return:代理IP
        """
        start_url = 'https://www.baibianip.com/home/free.html'
        html = downloader(url=start_url, method='GET')
        ip_pattern = re.compile(r"\('(.*)'\); </script></td>")
        port_pattern = re.compile(r'<td> (\d+) </td>')
        if html:
            ip_list = ip_pattern.findall(html, re.S)
            port_list = port_pattern.findall(html)
            for ips, port in zip(ip_list, port_list):
                ip = self.baibian_js(ips)
                results = ip + ':' + port
                # print(results)
                yield results

    def crawl_xicidaili(self):
        """
        西刺代理：https://www.xicidaili.com/
        封IP
        :return:
        """
        start_url = 'https://www.xicidaili.com/nn/{}'
        for page in range(1, 4):
            html = downloader(url=start_url.format(page), method='GET')
            if html:
                ip_pattern = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
                port_pattern = re.compile(r'<td>(\d+)</td>')
                ip_list = ip_pattern.findall(html)
                port_list = port_pattern.findall(html)
                for ip, port in zip(ip_list, port_list):
                    result = ip.strip() + ':' + port.strip()
                    # print(result)
                    yield result

    def crawl_cnip(self):
        """
        中国IP代理：http://cn-proxy.com/
        该网站无法访问
        :return:
        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "DNT": "1",
            "Host": "cn-proxy.com",
            "Referer": "https://www.google.com/",
            "Upgrade-Insecure-Requests": "1",
        }
        start_url = 'http://cn-proxy.com/'
        html = downloader(url=start_url, method='GET', headers=headers)
        if html:
            doc = pq(html)
            trs = doc('.sortable tbody tr').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1)').text().strip()
                port = tr.find('td:nth-child(2)').text().strip()
                result = ":".join([ip, port])
                # print(result)
                yield result

    # def crawl_quanwang(self):
    #     """
    #     全网代理：http://www.goubanjia.com/
    #     :return: 该网站解析有问题
    #     """
    #     start_url = 'http://www.goubanjia.com/'
    #     html = downloader(url=start_url, method='GET')
    #     if html:
    #         selector = etree.HTML(html)
    #         ip_a = selector.xpath('//td[@class="ip"]')
    #         for data in ip_a:
    #             print(data.xpath('string(.)'))


if __name__ == '__main__':
    """
    测试单个函数注释掉yield
    """
    obj = Crawler()
    obj.crawl_baibian()


