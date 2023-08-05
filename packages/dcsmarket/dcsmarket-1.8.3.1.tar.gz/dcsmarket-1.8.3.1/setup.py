# coding=utf-8
# !/usr/bin/python

"""
@Author: jeevan
@微信公众号: 大操手量化投资
@Site: http://dacaoshou.com
@Software: pycharm
@File：setup.py.py
@Time：2021/4/2 15:14
@Description: 
"""
from distutils.core import setup
from setuptools import find_packages

setup(name='dcsmarket',  # 包名
      version='1.8.3.1',  # 版本号
      description='大操手量化投资，股票行情数据接口',
      long_description='大操手量化投资，股票行情数据接口',
      author='大操手量化投资',
      author_email='yecaimeiv1@163.com',
      url='https://dacaoshou.com',
      license='',
      install_requires=['pandas'],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Utilities'
      ],
      keywords=['stock','data','大操手'],
      packages=['dcsmarket'],  # 必填，就是包的代码主目录
      include_package_data=True,
      )
# !/usr/bin/env python
