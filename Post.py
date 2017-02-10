#!/usr/bin/env python
# coding=utf-8

import requests, re
class Post(object):

    URL = 'http://bbs.tianya.cn/post-funinfo-{post_id}-{page_num}.shtml'

    """
    抓取指定uid发布的所有帖子：
    地址在：'http://www.tianya.cn/m/home.jsp?uid={uid}'.format(uid=6812290)
    """

    def __init__(self, post_id):
        # self.uid = int(post_id)
        self.post_id = post_id
        self.url = self.URL.format(post_id=int(post_id), page_num = 1)
        self.html = requests.get(self.url).text

    @property
    def id(self):
        return self.post_id

    @property
    def title(self):
        m = re.search(r'<span\sclass=\"s_title\"><span.*>(.*)</span></span>', self.html)
        # print(m.group(0))
        return m.group(1)

    @property
    def authorId(self):
        m = re.search(r'authorId\s\:\s\"(\d+)\"', self.html)
        # print(m.group(0))
        return m.group(1)

    @property
    def authorName(self):
        m = re.search(r'authorName\s:\s\"(.*)\"', self.html)
        return m.group(1)

    @property
    def itemName(self):
        m = re.search(r'itemName\s:\s\"(.*)\"', self.html)
        return m.group(1)

    @property
    def item(self):
        m = re.search(r'item\s:\s\"(.*)\"', self.html)
        return m.group(1)

    @property
    def date(self):
        m = re.search(r'<span>时间\：(.*)\s<\/span>', self.html)
        return m.group(1)

    @property
    def visit(self):
        m = re.search(r'<span>点击\：(.*)\s<\/span>', self.html)
        return m.group(1)

    @property
    def reply(self):
        """
        回复数，暂时只返回数字
        后期制作可返回reply对象
        """
        m = re.search(r'<span\stitle=\"共\d+个回帖和\d+个评论\">回复\：(\d+)</span>', self.html)
        return m.group(1)

    @property
    def replies(self):
        """
        回帖数
        """
        m = re.search(r'<span\stitle=\"共(\d+)个回帖和\d+个评论\">回复：\d+</span>', self.html)
        return m.group(1)

    @property
    def comments(self):
        """
        评论数
        """
        m = re.search(r'<span\stitle=\"共\d+个回帖和(\d+)个评论\">回复：\d+</span>', self.html)
        return m.group(1)


post = Post(7381834)
post.title

info = {
    'id':post.id,
    'title':post.title,
    'authorId':post.authorId,
    'authorName':post.authorName,
    'item':post.item,
    'itemName':post.itemName,
    'date':post.date,
    'visit':post.visit,
    'reply':post.reply,
    'replies':post.replies,
    'comments':post.comments,
}
print(info)
