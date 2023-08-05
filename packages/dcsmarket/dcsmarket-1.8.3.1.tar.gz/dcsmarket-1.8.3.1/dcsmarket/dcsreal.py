# coding=utf-8
# !/usr/bin/python

"""
@Author: jeevan
@微信公众号: 大操手量化投资
@Site: http://dacaoshou.com
@Software: pycharm
@File：dcsreal.py
@Time：2021/1/12 19:33
@Description: 
"""
import json

import requests

from dcsmarket import basequotation
import pandas as pd

from dcsmarket.helpers import get_stock_info_prefix, get_token

__all__ = ['DcsReal']
class DcsReal(basequotation.BaseQuotation):
    """
    "stockCode"：股票编码
    "stockName"：股票名称
    "tradeDate"：交易日期
    "time"：实时时间
    "current"：现价
    "open"：开盘价
    "high"：最高价
    "low"：最低价
    "preClosePrice"：昨收盘价
    "upLimitPrice"：涨停价
    "downLimitPrice"：跌停价
    "uptickPrice"：涨跌
    "uptickRate"：涨跌幅
    "surgeRate"：振幅
    "vol"：成交量
    "amount"：成交总额
    "committeeSent"：委差
    "buyPriceList"：委买五档盘口挂单价
    "buyVol"：委买五档盘口挂单量
    "askPriceList"：委卖五档盘口挂单价
    "askVol"：委卖五档盘口挂单量
    """
    max_num = 100

    def __init__(self):
        self.headers = {
            "token": get_token()
        }
        self._session = requests.session()

    @property
    def stock_api(self) -> str:
        return f"/api/data/stock/real-time?stockCodeArray="

    def _gen_stock_prefix(self, stock_codes):
        result = []
        for code in stock_codes:
            dcs_code = get_stock_info_prefix(code)
            result.append(dcs_code)
        return result

    def format_response_data(self, rep_data, prefix=False):
        # 多个股票
        result = pd.DataFrame()
        columns = ["stockCode", "stockName", "tradeDate", "time", "current", "open",
                   "high", "low", "preClosePrice", "upLimitPrice", "downLimitPrice", "stockCode",
                   "uptickPrice", "uptickRate", "surgeRate", "vol", "amount", "committeeSent",
                   "buyPriceList", "buyVol", "askPriceList", "askVol"]
        for item in rep_data:
            data_dict = json.loads(item)
            if data_dict['code'] != 200:
                print(data_dict["message"])
                return
            data = data_dict['data']
        return data
