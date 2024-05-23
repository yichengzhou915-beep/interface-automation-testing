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


case_id = ['im_01', 'im_02', 'im_03', 'im_04', 'im_05', 'im_06', 'im_07', 'im_08']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


@allure.epic("接口自动化")
@allure.feature("聊天模块")
class TestIm:

    @allure.story("im相关接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_im(self, in_data, case_skip):
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
    pytest.main(['test_test_im.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
