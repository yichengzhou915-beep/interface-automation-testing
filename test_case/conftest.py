#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
import hashlib
import random
import uuid
from urllib.parse import urlencode
import pytest
import time
import allure
import requests
import ast
from common.setting import ensure_path_sep
from utils.requests_tool.request_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.other_tools.models import TestCase
from utils.read_files_tools.clean_files import del_file
from utils.other_tools.allure_data.allure_tools import allure_step, allure_step_no
from utils.cache_process.cache_control import CacheHandler
from utils import config


@pytest.fixture(scope="session", autouse=False)
def clear_report():
    """如clean命名无法删除报告，这里手动删除"""
    del_file(ensure_path_sep("\\report"))


@pytest.fixture(scope="function", autouse=True)
def authorization(time_difference=0):
    params = {
        "appid": config.app_id,
        "timestamp": int(time.time()),
        "rand": random.randint(100000, 999999)
    }
    sorted_params = dict(sorted(params.items()))
    sorted_params['key'] = config.app_secret
    # 将参数字典转换为 URL 编码的查询字符串，并生成 MD5 哈希值
    query_string = urlencode(sorted_params)
    signature = hashlib.md5(query_string.encode('utf-8')).hexdigest()
    signature= signature.lower()
    rand = params['rand']
    timestamp = params['timestamp']
    url = config.host + '/v1/session/password'
    data = {"mobile": config.mobile,
            "password": config.password,
            "appid": config.app_id,
            "cid": "E08A92DB-E16B-0B6A-FC18-70BE4FE3F8B5",
            "sign": signature,
            "rand": rand,
            "timestamp": timestamp
            }
    res = requests.post(url, data)
    res = json.loads(res.text)
    access_token = res['data']['access_token']
    uid = res['data']['client']['uid']
    gear_id = res['data']['client']['gear_id']
    auth_string = f'{config.app_id}:{access_token}:{uid}:{gear_id}'
    authentication = 'USERID ' + base64.b64encode(auth_string.encode()).decode()
    split_token = authentication.split("USERID ")[1]
    uid = base64.b64decode(split_token).decode().split(":")[2]
    timestamp = int(time.time() * 1000) + time_difference
    nonce = str(uuid.uuid4()).replace('-', '')[:32]
    sign = hashlib.md5((config.app_id + str(timestamp) + nonce + uid + config.app_secret).encode('utf-8')).hexdigest()
    auth_string = f"{config.app_id}:{timestamp}:{nonce}:{uid}:{sign}"
    hua5_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    headers = {"authentication": authentication,
               "appSerial": config.appSerial,
               "hua5-auth": hua5_auth,
               "content-type": 'application/json;charset=UTF-8',
               "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1 wechatdevtools/1.06.2407110 MicroMessenger/8.0.5 webview/'
              }
    CacheHandler.update_cache(cache_name='headers', value=headers)
    print(headers)


# def work_login_init():
#     """
#     获取登录的cookie
#     :return:
#     """
#     url = config.host + '/v1/api/user/app/auth'
#     data = {
#         "phone": "18988494026",
#         "smsCode": "1812"
#     }
#     headers = {'Content-Type': 'application/json'}
#     try:
#         # 请求登录接口
#         res = requests.post(url=url, json=data, headers=headers)
#         res.raise_for_status()  # 检查响应是否成功
#         res = res.text
#         authorization = json.loads(res)['accessToken']
#         print(authorization)
#         if authorization:
#             CacheHandler.update_cache(cache_name='authorization', value=authorization)
#     except Exception as e:
#         pytest.fail(f"登录失败：{str(e)}")
#     # response_cookie = res.cookies
#     #
#     # cookies = ''
#     # for k, v in response_cookie.items():
#     #     _cookie = k + "=" + v + ";"
#     #     # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
#     #     cookies += _cookie
#     #     # 将登录接口中的cookie写入缓存中，其中login_cookie是缓存名称
#     # CacheHandler.update_cache(cache_name='login_cookie', value=cookies)


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的 item 的 name 和 node_id 的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    # 期望用例顺序
    # print("收集到的测试用例:%s" % items)
    appoint_items = ["test_get_user_info", "test_collect_addtool", "test_Cart_List", "test_ADD", "test_Guest_ADD",
                     "test_Clear_Cart_Item"]

    # 指定运行顺序
    run_items = []
    for i in appoint_items:
        for item in items:
            module_item = item.name.split("[")[0]
            if i == module_item:
                run_items.append(item)

    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)

        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]


def pytest_configure(config):
    config.addinivalue_line("markers", 'smoke')
    config.addinivalue_line("markers", '回归测试')


@pytest.fixture(scope="function", autouse=True)
def case_skip(in_data):
    """处理跳过用例"""
    in_data = TestCase(**in_data)
    if ast.literal_eval(cache_regular(str(in_data.is_run))) is False:
        allure.dynamic.title(in_data.detail)
        allure_step_no(f"请求URL: {in_data.is_run}")
        allure_step_no(f"请求方式: {in_data.method}")
        allure_step("请求头: ", in_data.headers)
        allure_step("请求数据: ", in_data.data)
        allure_step("依赖数据: ", in_data.dependence_case_data)
        allure_step("预期数据: ", in_data.assert_data)
        pytest.skip()


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    INFO.logger.error(f"用例总数: {_TOTAL}")
    INFO.logger.error(f"异常用例数: {_ERROR}")
    ERROR.logger.error(f"失败用例数: {_FAILED}")
    WARNING.logger.warning(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")
    try:
        _RATE = _PASSED / _TOTAL * 100
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")
