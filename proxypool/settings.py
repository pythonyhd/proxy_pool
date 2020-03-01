# -*- coding: utf-8 -*-


# --------------redis连接配置-----------------#
HOST = '127.0.0.1'
PORT = 6379
DB = 15
PASSWORD = ''

# --------------代理分数设置-----------------#
MAX_SCORE = 10  # 测试通过给得分数
MIN_SCORE = 0
INITIAL_SCORE = 6  # 第一次爬取成功ip，给得score设置成该值
REDIS_KEY = 'freeproxies'
# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 测试器测试api，最好抓取哪个网站测试哪个网站，检测网站只能是http的，aiohttp异步检测库不支持https的
TEST_URL = 'http://httpbin.org/get'
# TEST_URL = 'http://icanhazip.com/'

# 遇到以下状态码，测试通过，认定为可用IP
VALID_STATUS_CODES = [200, 201, 202]
# 最大批测试量
BATCH_TEST_SIZE = 10

# 检测器休眠时间，检查的周期
TESTER_CYCLE = 20  # 每隔20秒检测一次ip能不能用
# 获取器休眠时间，抓取ip周期
GETTER_CYCLE = 300

# 检测器开关
TESTER_ENABLED = True
# 获取器开关
GETTER_ENABLED = True
# flask开关
API_ENABLED = False
# API配置
API_HOST = '127.0.0.1'
API_PORT = 5555
