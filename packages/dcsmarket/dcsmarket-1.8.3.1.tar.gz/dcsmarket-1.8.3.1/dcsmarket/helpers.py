# coding:utf8
"""
@Author: liao
@微信公众号: 大操手量化投资
@Site: http://dacaoshou.com
@Software: pycharm
@Time：2021/4/2 15:14
@Description:
"""
import json
import os

import pandas as pd
import requests

STOCK_CODE_PATH = os.path.join("all_stock.csv")


def update_stock_codes():
    """获取所有股票 ID 到 all_stock_code 目录下"""
    try:
        headers = {
            "token": get_token()
        }
        _session = requests.session()
        response = _session.get("https://dacaoshou.com/api/data/stock/get_all_stock_info", headers=headers)
        data = json.loads(response.text)
        if data.get("code") != 0:
            print("获取股票基础数据失败，返回信息：{}，使用上次数据.".format(data.get("code")))
            return pd.DataFrame(STOCK_CODE_PATH)
        columns = ["dcsCode", "stockCode", "name", "area", "industry", "listedDate", "isHs"]
        p_data = pd.DataFrame(data.get("data"), columns=columns)
        p_data.to_csv(STOCK_CODE_PATH)
        return p_data
    except:
        print("获取股票基础数据失败，使用上次数据.")
    return pd.read_csv(STOCK_CODE_PATH)


def get_stock_codes(realtime=False):
    if realtime:
        return update_stock_codes()
    p_data = pd.DataFrame(STOCK_CODE_PATH)
    return p_data

def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert type(stock_code) is str, "stock code need str type"
    sh_head = ("50", "51", "60", "90", "110", "113",
               "132", "204", "5", "6", "9", "7")
    if stock_code.startswith(("sh", "sz", "zz")):
        return stock_code[:2]
    else:
        return "sh" if stock_code.startswith(sh_head) else "sz"


def get_stock_info(stock_code):
    assert type(stock_code) is str, "请输入字符串类型的编码"
    sh_head = ("50", "51", "60", "90", "110", "113",
               "132", "204", "5", "6", "9", "7")
    code = stock_code
    if stock_code.startswith(("sh", "sz")):
        code = stock_code[2:]
    if code.startswith(sh_head):
        return code, "SH", 1
    else:
        return code, "SZ", 2


def get_stock_info_prefix(stock_code):
    assert type(stock_code) is str, "请输入字符串类型的编码"
    sh_head = ("50", "51", "60", "90", "110", "113",
               "132", "204", "5", "6", "9", "7")
    if stock_code.startswith(("sh", "sz")):
        return stock_code
    if stock_code.startswith(sh_head):
        return "sh" + stock_code
    else:
        return "sz" + stock_code


def set_token(token):
    df = pd.DataFrame([token.strip()], columns=['token'])
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, 'dcs_token.csv')
    df.to_csv(fp, index=False)


def get_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, 'dcs_token.csv')
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        return str(df.loc[0]['token'])
    else:
        print("token校验失败，请使用token获取数据，token获取请访问：https://dacaoshou.com")
        return None


def load_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, 'dcs_token.csv')
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        return str(df.loc[0]['token'])
    else:
        return None
