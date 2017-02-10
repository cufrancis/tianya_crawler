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

    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text

    @property
    def id(self):
        m = re.search(r'\"merNum\"\:\"(\d+)\"', self.html)
        return int(m.group(1))

    @property
    def name(self):
        p = re.compile(r'userName\:\s\'(.*)\'')
        m = p.search(self.html)
        return m.group(1)

    @property
    def gender(self):
        p = re.compile(r'gender\:\s\'(.*)\'')
        m = p.search(self.html)
        return m.group(1)

    @property
    def regTime(self):
        p = re.compile(r'regTime\:\'(.*)\'')
        m = re.search(r'regTime\:\'(.*)\'', self.html)
        # print(m.group(0))
        return m.group(1)



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

        p = re.compile(r'alt=\"{name}\"\ssrc=\"(.*)\"\s\/>'.format(name=self.name))
        m = p.search(self.html)
        urlretrieve(m.group(1), avatar_dir)

        return avatar_dir

    @property
    def follow(self):
        m = re.search(r'\<a\shref=\".*\/follow\"\>(\d+)\<\/a\>', self.html)
        return int(m.group(1))

    @property
    def fans(self):
        m = re.search(r'\<a\shref=\".*\/fans\"\>(\d+)\<\/a\>', self.html)
        return int(m.group(1))

    @property
    def integral(self):
        m = re.search(r'积&#12288;&#12288;分\<\/span\>(\d+)\<', self.html)
        return int(m.group(1))
        # print(m.group(0))
    @property
    def loginNum(self):
        m = re.search(r'登陆次数\<\/span\>(\d+)\<', self.html)
        return int(m.group(1))

    @property
    def newLogin(self):
        m = re.search(r'最新登陆\<\/span\>(\d+)\<', self.html)
        return int(m.group(1))

    @property
    def birthday(self):
        m = re.search(r'<li><i class=\"user-bir\"></i>(.*)</li>', self.html)
        return m.group(1)

    @property
    def note(self):
        m = re.search(r'<li><i class=\"user-note\"></i>(.*)</li>', self.html)
        return m.group(1)

    def posts(self):
        pass

    def reply(self):
        """
        回复
        """
        pass

user = User('http://www.tianya.cn/20484397')
user.avatar
info = {
    'id':user.id,
    'name':user.name,
    'gender':user.gender,
    'avatar':user.avatar,
    'regTime':user.regTime,
    'follow':user.follow,
    'fans':user.fans,
    'integral':user.integral,
    'birthday':user.birthday,
    'note':user.note,
}
print(info)
