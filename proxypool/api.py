# -*- coding: utf-8 -*-
"""
flask对接redis数据库，执行相应的操作，g保存的是应用层面的全局变量，request保存的是请求上下文的变量。
"""
from flask import Flask, g
from flask import request
from proxypool.db import RedisClient

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):  # 用于判断对象是否包含对应的属性
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h1><p  style="width: 100%;height: 45px;display: block;line-height: 45px;text-align: center;">欢迎来到华东的代理池系统</p></h1>'


@app.route('/random')
def get_random_ip():
    """ 随机获取ip """
    connection = get_conn()
    return connection.random()


@app.route('/count')
def get_counts():
    """ Get the count of proxies """
    conn = get_conn()
    return str(conn.count())


@app.route('/put')
def upload_proxy():
    """ 将proxy上传到redis数据库中 """
    conn = get_conn()
    proxy = request.args.get("proxy")
    remote_ip = request.remote_addr
    port = proxy.split(":")[1]
    proxy = "{}:{}".format(remote_ip, port)
    if not proxy:
        return "上传代理不能为空"
    conn.add(proxy)
    return "已成功上传代理: {}".format(proxy)


@app.route('/remove')
def remove_proxy():
    """ 删除代理 """
    conn = get_conn()
    proxy = request.args.get('proxy', '')
    if not proxy:
        return '代理不能为空'
    conn.delete(proxy)
    return "已成功删除代理:{}".format(proxy)


if __name__ == '__main__':
    app.run()