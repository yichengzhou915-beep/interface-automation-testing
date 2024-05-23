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


case_id = ['content_01', 'content_02', 'content_03', 'content_04', 'content_05', 'content_06', 'content_07', 'content_08', 'content_09', 'content_10', 'content_11', 'content_12', 'content_13', 'content_14', 'content_15', 'content_16', 'content_17', 'content_18', 'content_19', 'content_20', 'content_21', 'content_22', 'content_23', 'content_24', 'content_25', 'content_26', 'content_27', 'content_28', 'content_29', 'content_30', 'content_31', 'content_32', 'content_33', 'content_34', 'content_35', 'content_36', 'content_37', 'content_38', 'content_39', 'content_40', 'content_41', 'content_42', 'content_43', 'content_44', 'content_45', 'content_46', 'content_47', 'content_48']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


@allure.epic("接口自动化")
@allure.feature("首页模块")
class TestContent:

    @allure.story("文章相关接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_content(self, in_data, case_skip):
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
    pytest.main(['test_test_content.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
