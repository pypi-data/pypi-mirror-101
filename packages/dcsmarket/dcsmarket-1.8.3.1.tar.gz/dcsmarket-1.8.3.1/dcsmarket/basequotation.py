# coding:utf8
"""
@Author: cat
@微信公众号: 大操手量化投资
@Site: http://dacaoshou.com
@Software: pycharm
@Time：2021/4/2 15:14
@Description:
"""
import abc
import json
import multiprocessing.pool
import warnings

import requests

from dcsmarket.helpers import get_token
from . import helpers

class BaseQuotation(metaclass=abc.ABCMeta):
    """行情获取基类"""
    max_num = 800  # 每次请求的最大股票数

    @property
    def dcs_domain(self) -> str:
        return "https://dacaoshou.com"

    @property
    @abc.abstractmethod
    def stock_api(self) -> str:
        pass

    def __init__(self):
        self.headers = {
            "token": get_token()
        }
        self._session = requests.session()
        stock_codes = self.load_stock_codes()
        self._can_multi = True
        self.stock_list = self.gen_stock_list(stock_codes)

    def gen_stock_list(self, stock_codes):
        stock_with_exchange_list = self._gen_stock_prefix(stock_codes)

        if self.max_num > len(stock_with_exchange_list):
            request_list = ",".join(stock_with_exchange_list)
            return [request_list]

        stock_list = []
        for i in range(0, len(stock_codes), self.max_num):
            request_list = ",".join(
                stock_with_exchange_list[i : i + self.max_num]
            )
            stock_list.append(request_list)
        return stock_list

    def _gen_stock_prefix(self, stock_codes):
        return [
            helpers.get_stock_type(code) + code[-6:] for code in stock_codes
        ]

    @staticmethod
    def load_stock_codes():
        with open(helpers.STOCK_CODE_PATH) as f:
            return json.load(f)["stock"]

    @property
    def all(self):
        warnings.warn("use market_snapshot instead", DeprecationWarning)
        return self.get_stock_data(self.stock_list)

    @property
    def all_market(self):
        return self.get_stock_data(self.stock_list, prefix=True)

    def stocks(self, stock_codes, prefix=False):
        """
        :param stock_codes: 股票数组，例如：["601988","600018"]
        :return:
        """
        return self.real(stock_codes, prefix)

    def real(self, stock_codes, prefix=False):
        if not isinstance(stock_codes, list):
            stock_codes = [stock_codes]

        stock_list = self.gen_stock_list(stock_codes)
        return self.get_stock_data(stock_list, prefix=prefix)

    def market_snapshot(self, prefix=False):
        return self.get_stock_data(self.stock_list, prefix=prefix)

    def get_stocks_by_range(self, params):
        try:
            headers = {
                "Accept-Encoding": "gzip, deflate, sdch"
            }
            headers.update(self.headers)
            if self.stock_api.find("http://")>=0 or self.stock_api.find("https://")>=0:
                _stock_api = self.stock_api
            else:
                _stock_api = self.dcs_domain+self.stock_api
            r = self._session.get(_stock_api + params, headers=headers)
            return r.text
        except:
            print("获取数据失败，参数：{}".format(params))
            return None

    def get_stock_data(self, stock_list, **kwargs):
        """获取并格式化股票信息"""
        res = self._fetch_stock_data(stock_list)
        return self.format_response_data(res, **kwargs)

    def _fetch_stock_data(self, stock_list):
        """获取股票信息"""
        pool = multiprocessing.pool.ThreadPool(len(stock_list))
        try:
            res = pool.map(self.get_stocks_by_range, stock_list)
        finally:
            pool.close()
        return [d for d in res if d is not None]

    def format_response_data(self, rep_data, **kwargs):
        pass
