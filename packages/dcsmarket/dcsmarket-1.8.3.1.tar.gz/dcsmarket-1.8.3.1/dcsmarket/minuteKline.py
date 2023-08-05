# coding=utf-8
# !/usr/bin/python

"""
@Author: liao
@微信公众号: 大操手量化投资
@Site: http://dacaoshou.com
@Software: pycharm
@File：minuteKline.py
@Time：2021/1/10 19:54
@Description: 
"""
import json

import requests

import pandas as pd
from dcsmarket.helpers import get_stock_info
from dcsmarket.helpers import get_token
from . import basequotation


class MinuteKline(basequotation.BaseQuotation):
    # 每次请求只能允许一个
    max_num = 1

    def __init__(self, minuteType, nodeCount):
        self.headers = {
            "token": get_token()
        }
        self._session = requests.session()
        self.minuteType = minuteType
        self.nodeCount = nodeCount
        self._can_multi = False

    @property
    def stock_api(self) -> str:
        return "/api/data/stock/k-line-minute?"

    def _gen_stock_prefix(self, stock_codes):
        result = []
        for code in stock_codes:
            code, marketCode, stockMarket = get_stock_info(code)
            param = "stockCode={}&minuteType={}&nodeCount={}&marketCode={}&stockMarket={}".format(code, self.minuteType,
                                                                                                  self.nodeCount,
                                                                                                  marketCode,
                                                                                                  stockMarket)
            result.append(param)
        return result

    def format_response_data(self, rep_data, **kwargs):
        # 多个股票
        stock_dict = {}
        columns = ["dateTime", "tradeDate", "time", "open", "high", "low", "close", "vol"]
        for item in rep_data:
            data_dict = json.loads(item)
            if data_dict['code'] != 200:
                print(data_dict["message"])
                return
            data = data_dict['data']
            p_data = pd.DataFrame(data["klineData"], columns=columns)
            p_data["stockCode"] =data["stockCode"]
            stock_dict.update({
                data["stockCode"]: p_data
            })
        return stock_dict
