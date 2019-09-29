# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 15:14
# @Author  : Yasaka.Yu
# @File    : run.py
from proxypool.scheduler import Scheduler
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        scheduler = Scheduler()
        scheduler.run()
    except Exception as e:
        print(repr(e.args))
        main()


if __name__ == '__main__':
    main()