#!/usr/bin/env python
# coding=utf-8

class Post(object):

    """
    抓取指定uid发布的所有帖子：
    地址在：'http://www.tianya.cn/m/home.jsp?uid={uid}'.format(uid=6812290)
    """

    def __init__(self, uid):
        self.uid = int(uid)
