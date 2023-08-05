# coding:utf8
from . import real, minuteKline, kline,dcsreal


def use(source:str, minuteType:int=5, nodeCount:int=10, fqType:int=None, dateType:int=1):
    """
    :param source: 获取数据源类型：minuteKline=分钟线; kline=日线; real=实时行情及五档盘口
    :param minuteType: 分钟线周期，可获取分钟：5, 15, 30, 60
    :param nodeCount: 获取k线个数：一次最多600
    :param fqType:日K线复权类型：不填，则默认不复权；1，前复权；2，后复权
    :param dateType:日K线类型：不填则 默认 1,日线；2，周线；3，月线
    """
    if source in ["real"]:
        return real.Real()
    if source in ["dcsReal"]:
        return dcsreal.DcsReal()
    if source in ["minuteKline"]:
        return minuteKline.MinuteKline(minuteType=minuteType, nodeCount=nodeCount)
    if source in ["dayKline"]:
        return kline.Kline(fqType=fqType, dateType=dateType, nodeCount=nodeCount)
    raise NotImplementedError