# -*- coding: utf-8 -*-
import time

from multiprocessing import Process

from proxypool.settings import TESTER_CYCLE, GETTER_CYCLE
from proxypool.tester import ValidityTester
from proxypool.getter import Getter
from proxypool.settings import TESTER_ENABLED, GETTER_ENABLED, API_ENABLED, API_HOST, API_PORT
from proxypool.api import app


class Scheduler(object):
    def tester_scheduler(self, cycle=TESTER_CYCLE):
        """ 定时调度，检测器 """
        tester = ValidityTester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def getter_scheduler(self, cycle=GETTER_CYCLE):
        """ IP获取器 """
        getter = Getter()
        while True:
            print('ip数量不足，获取器开始运行')
            getter.run()
            time.sleep(cycle)

    def api_scheduler(self):
        """ flask服务api调度 """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理调度器主函数运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.tester_scheduler)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.getter_scheduler)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.api_scheduler)
            api_process.start()