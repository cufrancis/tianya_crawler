#!/usr/bin/env pyuthon
# coding=utf-8

import requests, re
from bs4 import BeautifulSoup
from Db import db
from User import User
import sys

class Splider(object):
    """
    爬虫主类，主要功能：
    提取网页上的所有超链接，并提取uid和post_id
    调用User和Post类根据提取的数据抓取信息
    最后存入数据库
    """
    def __init__(self, url="http://bbs.tianya.cn/post-funinfo-7381834-1.shtml"):
        self.url = url
        self.db = db
        self.html = self._get_html()

    def _get_html(self):
        html = requests.get(self.url)
        html.encoding = 'utf-8'
        return html.text

    def user(self):
        """
        提取网页上的所有uid
        """
        data = list()
        tmp = re.findall(r'http://www.tianya.cn/(\d+)', self.html)
        tmp = list(set(tmp))

        for k in tmp:
            data.append(int(k))

        print(data)

    def run(self):
        """
        开始运行爬虫，主要编写并发程序，调度crawl_uid与crawl_info函数
        """
        pass

    def crawl_uid(self):
        """
        提取网页上的所有uid
        """
        data = list()
        tmp = re.findall(r'http://www.tianya.cn/(\d+)', self.html)
        tmp = list(set(tmp))

        for k in tmp:
            data.append(int(k))

        return self.db.noCrawl(data)


    def crawl_info(self):
        """
        从数据库中提取uid,并爬取指定数据存入数据库
        持续运行，知道数据库中无uid为止
        """

        if self.db.spop() is None:
            return "全部数据已抓取完成!"
        uid = self.db.spop()

        if uid is not None:
            print('uid:{uid} Start...\r'.format(uid=uid),)
            user = User(uid)
            # print(user.id)
            info = {
                'uid':user.id,
                'name':user.name,
                'gender':user.gender,
                'avatar':user.avatar,
                'regTime':user.regTime,
                'loginNum':user.loginNum,
                'newLogin':user.newLogin,
                'follow':user.follow_num,
                'fans':user.fans_num,
                'integral':user.integral,
                'birthday':user.birthday,
                'income':user.income,
                'graph':user.graph,
                'rank_number':user.rank_number,
                'note':user.note,
            }

            if self.db.insert_user(info):
                print("..............OK!\r",)
                sys.stdout.flush()
                return uid
            else:
                print("..............Fault!")
                return False
        else:
            print("..............Fault!")
            return False

splider = Splider()

while(True):
    splider.crawl_uid()
    splider.crawl_info()

# print(result)
# print(splider.db.get_user(65016273)['name'])
# splider.crawl()
