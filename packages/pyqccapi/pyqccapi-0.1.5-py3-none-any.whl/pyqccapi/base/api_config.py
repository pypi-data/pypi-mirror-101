import os

import pywildcard
import requests

from pyqccapi.util.jsons import *


class ApiConfig:
    """
    配置相关类
    用于https://www.qcc.com的category,api,method及其详情的同步
    同时提供全局唯一的api相关配置信息管理
    """

    path_api_config = os.path.dirname(os.path.abspath(__file__))

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7",
        "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIiLCJjcmVhdGVUaW1lIjoxNjA5NTEwNDI2LCJhY2NvdW50Tm8iOiIxODkxNzYxODUwOSIsImlzcyI6IlNhY2hpZWwuWmhhbyIsInVzZXJJZCI6ImUzMTJmMWRkN2Q4M2U0ZDQyM2IyODg2NzY5ZjZjYWY1In0.gaKAuPN2Z0i92dFE6rpbCWxTHoiWUL3F0zp4S9DuRJg",
        "content-type": "application/x-www-form-urlencoded",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "Hm_lvt_5cd3bf91755d53008b430f15579b08c6=1609471544; _uab_collina=160947879460966050149085; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIiLCJjcmVhdGVUaW1lIjoxNjA5NTEwNDI2LCJhY2NvdW50Tm8iOiIxODkxNzYxODUwOSIsImlzcyI6IlNhY2hpZWwuWmhhbyIsInVzZXJJZCI6ImUzMTJmMWRkN2Q4M2U0ZDQyM2IyODg2NzY5ZjZjYWY1In0.gaKAuPN2Z0i92dFE6rpbCWxTHoiWUL3F0zp4S9DuRJg; shopCartCnt=0; UserBalance=399.9; isUserAuthentication=false; Hm_lpvt_5cd3bf91755d53008b430f15579b08c6=1609511337; getCurrentDataNav=6c02d82a-ebcc-4a3a-a933-49a4ea5e4087"
    }

    _cfg = None

    @classmethod
    def to_instance(cls):
        if ApiConfig._cfg is None:
            ApiConfig._cfg = ApiConfig()
        return ApiConfig._cfg

    def __init__(self):
        ApiConfig._cfg = self
        self.method_dict = {}
        self.method_list = []
        self.of_config_files().to_method_dict()

    def to_category_list_file(self):
        url = 'https://openapi.qcc.com/API/DataApi/index'
        r = requests.post(url=url, headers=self.headers)
        if r.status_code == 200:
            result = r.json()['result']
            to_json_file(os.path.join(self.path_api_config, 'category_list.json'), result)
        return self

    def to_api_list_file(self):
        url = 'https://openapi.qcc.com/API/DataApi/getApiList'
        data = {
            'pageNum': 1,
            'pageSize': 1000,
            'apiType': 'cate_all'
        }
        r = requests.post(url=url, headers=self.headers, data=data)
        if r.status_code == 200:
            api_list = r.json()['result']['apiPage']['list']
            to_json_file(os.path.join(self.path_api_config, 'api_list.json'), api_list)
        return self

    def to_method_base_list_file(self):
        url = 'https://openapi.qcc.com/API/DataApiDetail/getApiMethodTree'
        data = {
            'apiId': ''
        }
        method_list = []
        api_list = of_json_file(os.path.join(self.path_api_config, 'api_list.json'))
        for api in api_list:
            data['apiId'] = api['Id']
            r = requests.post(url=url, headers=self.headers, data=data)
            if r.status_code == 200:
                methods = r.json()['result']
                for method in methods:
                    method['apiId'] = api['Id']
                    method['apiTitle'] = api['Title']
                    method_list.append(method)
            else:
                print(r.status_code)
        to_json_file(os.path.join(self.path_api_config, 'method_list.json'), method_list)
        return self

    def to_method_detail_list_file(self):
        url = 'https://openapi.qcc.com/API/DataApiDetail/getApiMethodDetailInfo'
        data = {
            'apiId': '',
            'methodApiId': ''
        }
        method_detail_list = []
        method_list = of_json_file(os.path.join(self.path_api_config, 'method_list.json'))
        for method in method_list:
            data['apiId'] = method['apiId']
            data['methodApiId'] = method['methodApiId']
            r = requests.post(url=url, headers=self.headers, data=data)
            if r.status_code == 200:
                detail = r.json()['result']
                detail['Method'] = method
                method_detail_list.append(detail)
            else:
                print(r.status_code)
        to_json_file(os.path.join(self.path_api_config, 'method_detail_list.json'), method_detail_list)
        return self

    # def to_method_url_dict(self):
    #     method_url_dict = {}
    #     method_detail_list = of_json_file('method_detail_list.json')
    #     for method_detail in method_detail_list:
    #         method_url_dict[method_detail['Method']['methodApiId']] = method_detail['Titles']['paramList']['apiUrl']
    #     return method_url_dict

    # def view_method(self, pattern):
    #     result = []
    #     method_list = of_json_file('method_list.json')
    #     for method in method_list:
    #         if pywildcard.fnmatch(method['methodApiName'], pattern) or pywildcard.fnmatch(method['apiTitle'], pattern):
    #             result.append(method)
    #     format_json(result)

    def view_method_detail(self, pattern: str):
        result = []
        for method_detail in self.method_list:
            if pywildcard.fnmatch(method_detail['Method']['methodApiName'], pattern) or \
                    pywildcard.fnmatch(method_detail['Method']['apiTitle'], pattern):
                result.append(method_detail)
        format_json(result)

    def to_method_detail(self, method_id: str):
        return self.method_dict[method_id]

    def to_config_files(self):
        return self.to_category_list_file(). \
            to_api_list_file(). \
            to_method_base_list_file(). \
            to_method_detail_list_file()

    def of_config_files(self):
        path_method_detail_json = os.path.join(self.path_api_config, 'method_detail_list.json')
        if not os.path.exists(path_method_detail_json):
            self.to_config_files()
        self.method_list = of_json_file(path_method_detail_json)
        return self

    def to_method_dict(self):
        for method_detail in self.method_list:
            self.method_dict[method_detail['Method']['methodApiId']] = method_detail
        return self


# ApiConfig.to_instance().view_method_detail("客户查询")
