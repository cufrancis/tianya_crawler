#!/usr/bin/env pyuthon
# coding=utf-8

import requests, re
from bs4 import BeautifulSoup

class Splider(object):
    """
    爬虫主类，主要功能：
    提取网页上的所有超链接，并提取uid和post_id
    调用User和Post类根据提取的数据抓取信息
    最后存入数据库
    """
    def __init__(self, url="http://focus.tianya.cn/"):
        self.url = url
        self.html = self._get_html()

    def _get_html(self):
        html = requests.get(self.url)
        # html.encoding = 'utf-8'
        return html

splider = Splider()
splider.a()
