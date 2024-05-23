#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023-10-03 22:34:14


import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.requests_tool.request_control import RequestControl
from utils.read_files_tools.regular_control import regular
from utils.requests_tool.teardown_control import TearDownHandler


case_id = ['my_01', 'my_02', 'my_03', 'my_04', 'my_05', 'my_06', 'my_07', 'my_08', 'my_09', 'my_10', 'my_11', 'my_12', 'my_13', 'my_14', 'my_15', 'my_16', 'my_17', 'my_18', 'my_19', 'my_20', 'my_21', 'my_22', 'my_23', 'my_24', 'my_25', 'my_26', 'my_27', 'my_28', 'my_29', 'my_30', 'my_31']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


@allure.epic("接口自动化")
@allure.feature("我的模块")
class TestMy:

    @allure.story("我的菜单下接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_my(self, in_data, case_skip):
        """
        :param :
        :return:
        """
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(assert_data=in_data['assert_data'],
               sql_data=res.sql_data,
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()


if __name__ == '__main__':
    pytest.main(['test_test_my.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
