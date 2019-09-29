# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 11:41
# @Author  : Yasaka.Yu
# @File    : error.py


class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')