#!/usr/bin/env pyuthon
# coding=utf-8


import requests
import re
import os
from urllib.request import urlopen, urlretrieve

class User(object):

    """
    根据指定url获取用户的所有信息
    """

    def __init__(self, uid):
        self.uid = int(uid)
        self.url = 'http://www.tianya.cn/{uid}'.format(uid=self.uid)
        self.html = requests.get(self.url).text

    @property
    def id(self):
        return self.uid

    @property
    def name(self):
        return self._get(r'userName\:\s\'(.*)\'')

    @property
    def gender(self):
        return self._get(r'gender\:\s\'(.*)\'')

    @property
    def regTime(self):
        return self._get(r'regTime\:\'(.*)\'')


    @property
    def avatar(self):
        """
        获取头像
        先从网页中提取头像url
        然后使用urllib的urlretrieve函数下载文件到指定文件夹下，文件名为{uid}.jpg
        返回保存的文件地址
        """
        path = "avatar"
        file_name = "{id}.jpg".format(id=self.id)
        avatar_dir = os.path.join(path, file_name)

        # p = re.compile(r'alt=\"{name}\"\ssrc=\"(.*)\"\s\/>'.format(name=self.name))
        # m = p.search(self.html)
        avatar = self._get(r'alt=\"{name}\"\ssrc=\"(.*)\"\s\/>'.format(name=self.name), '')

        if avatar == '':
            return ''
        else:
            urlretrieve(avatar, avatar_dir)
            return avatar_dir

    @property
    def follow_num(self):
        # m = re.search(r'\<a\shref=\".*\/follow\"\>(\d+)\<\/a\>', self.html)
        # return int(m.group(1))
        return int(self._get(r'\<a\shref=\".*\/follow\"\>(\d+)\<\/a\>', 0))

    def follow(self):
        """
        关注列表
        关注列表查询api接口：
        http://www.tianya.cn/api/tw?method=following.ice.select&params.userId=20484397&params.pageNo=1&params.pageSize=28
        和粉丝api一样，非用户本人或者Ta的好友，只能查询前100名关注人
        返回值为关注者id,类型为列表
        """
        pageSize = 50 # 每页50条数据
        api = 'http://www.tianya.cn/api/tw?method=following.ice.select&params.userId={uid}&params.pageNo=1&params.pageSize={pageSize}'.format(uid=self.uid, pageSize=pageSize)
        data = list()

        for k in [1, 2]:
            html = requests.get(api).text
            data.append(re.findall(r'\"id\"\:(\d+),', html))
        # 合并data数据到following_list中
        following_list = list()

        for k in data:
            for i in k:
                following_list.append(int(i))

        return following_list


    @property
    def fans_num(self):
        # m = re.search(, self.html)
        # return int(m.group(1))
        return int(self._get(r'\<a\shref=\".*\/fans\"\>(\d+)\<\/a\>', 0))

    def fans(self):
        """
        粉丝列表
        粉丝api接口:
        http://www.tianya.cn/api/tw?method=follower.ice.select&params.userId=20484397&params.pageNo=1&params.pageSize=28
        非用户本人或者Ta的好友，只能查询前100名粉丝，所以我们只提取100个id
        返回值为粉丝id，类型为列表
        """

        pageSize = 50 # 每页50条数据
        api = 'http://www.tianya.cn/api/tw?method=follower.ice.select&params.userId={uid}&params.pageNo=1&params.pageSize={pageSize}'.format(uid=self.uid, pageSize=pageSize)
        data = list()

        for k in [1, 2]:
            html = requests.get(api).text
            data.append(re.findall(r'\"id\"\:(\d+),', html))
        # 合并data数据到id list中
        fans_list = list()
        for k in data:
            for i in k:
                fans_list.append(int(i))

        return fans_list

    @property
    def integral(self):
        # m = re.search(, self.html)
        # return int(m.group(1))
        return int(self._get(r'积&#12288;&#12288;分\<\/span\>(\d+)\<', 0))

    @property
    def loginNum(self):
        # m = re.search(, self.html)
        # return int(m.group(1))
        return int(self._get(r'登录次数\<\/span\>(\d+)\<', 0))

    @property
    def newLogin(self):
        return self._get(r'最新登录\<\/span\>(.*)\<\/p\>')

    @property
    def birthday(self):
        return self._get(r'<li><i class=\"user-bir\"></i>(.*)</li>')

    @property
    def income(self):
        """
        收入赏金
        """

        # m = re.search(r'class\=\"income\">\s*<h3>收入赏金<\/h3>\s*<p>(\d+)<\/p>', self.html)
        # return m.group(1)
        return self._get(r'class\=\"income\">\s*<h3>收入赏金<\/h3>\s*<p>(\d+)<\/p>', 0)

    @property
    def note(self):
        return self._get(r'<li><i class=\"user-note\"></i>(.*)</li>')


    @property
    def graph(self):
        """
        收入排名，大概范围
        """
        # m = re.search(r'<div\sclass=\"ranking-graph\">\s*<p>(.*)</p>', self.html)
        # return m.group(1)
        return self._get(r'<div\sclass=\"ranking-graph\">\s*<p>(.*)</p>', 0)

    @property
    def rank_number(self):
        """
        排名百分比，排在多少网友前面
        """
        # m = re.search(r'排在<\/h3>\s*<p><span>(\d+)<\/span>\%网友前面</p>', self.html)
        # return m.group(1)
        return int(self._get(r'排在<\/h3>\s*<p><span>(\d+)<\/span>\%网友前面</p>', 0))

    def _get(self, regular, default=''):
        """
        根据regular提取网页中的内容
        default为出错时返回的默认值，默认为None
        """
        try:
            m = re.search(regular, self.html)
        except:
            return default
        else:
            # 判断是否从网页中抓取到数据
            if m == None:
                return default
            else:
                return m.group(1)

# user = User(117648301)
# info = {
#     'uid':user.id,
#     '昵称':user.name,
#     '性别':user.gender,
#     '头像':user.avatar,
#     '注册时间':user.regTime,
#     '登录次数':user.loginNum,
#     '最新登录':user.newLogin,
#     '关注数':user.follow(),
#     '粉丝数':user.fans_num,
#     '积分':user.integral,
#     '生日':user.birthday,
#     '收入赏金':user.income,
#     '收入排名':user.graph,
#     '网友排名':user.rank_number,
#     '个人笔记':user.note,
# }
# print(info)
