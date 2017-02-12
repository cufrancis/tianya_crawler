#!/usr/bin/env pyuthon
# coding=utf-8

import time
import requests, re
from Db import db
from User import User
import sys
from Console import console
from multiprocessing import Pool
from multiprocessing.dummy import Pool as mulThread

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

    def mulThreadTime(self, name, arg,nums=4):
        '''多线程计时'''
        pool = mulThread(processes=nums) #开启四个线程
        time3 = time.time()
        pool.map(name,arg)
        pool.close()
        pool.join() #等待线程池中的worker进程执行完毕
        time4 = time.time()
        return str(time4 - time3)


    def crawl_info(self):
        """
        从数据库中提取uid,并爬取指定数据存入数据库
        持续运行，知道数据库中无uid为止
        """

        if self.db.spop() is None:
            return "全部数据已抓取完成!"
        uid = self.db.spop()

        if uid is not None:
            # print('uid:{uid} Start...\r'.format(uid=uid),)
            console.info('uid:{uid} Start ...'.format(uid=uid), False)
            user = User(uid)

            pool = mulThread(processes=4) #开启四个线程
            time3 = time.time()
            pool.map(self.db.noCrawl,user.fans())
            pool.map(self.db.noCrawl,user.follows())
            pool.close()
            pool.join()
            time4 = time.time()
            times = str(time4-time3)
            console.success(times[0:5]+"s............", False)
            # time1 = self.mulThreadTime(self.db.noCrawl,user.fans())
            # console.success(time1)
            # time2 = self.mulThreadTime(self.db.noCrawl,user.follows())
            # console.success

            # self.db.noCrawl(user.fans())
            # self.db.noCrawl(user.follows())
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
                self.db.isCrawl(int(uid))
                # print("..............OK!\r",)
                console.success("[ok]", False)
                console.success(" count:{0}|noCrawl:{1}|Crowl:{2}|last:{3}".format(self.db.usersNum, self.db.noCrowlNum, self.db.CrowlNum, self.db.noCrowlNum-self.db.CrowlNum))
                # sys.stdout.flush()

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
