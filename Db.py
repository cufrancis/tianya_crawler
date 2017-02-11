#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from Console import console

class DB(object):
    ALL_USER = 'user_set' # 所有uid集合
    USER = 'user_{uid}' # 存储用户的数据
    CRAWL = 'crawl' # 已抓取的数据
    NO_CRAWL = 'no_crawl' # 未抓取的数据


    def __init__(self, host='localhost', port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.r = redis.StrictRedis(connection_pool=self.pool)

    # def __format__(self, format_spec):
    #     return format(str(self), format_spec)

    # def _format(self, name, spec):
    #     # return name.format(spec=spec)

    def all_users(self, data):
        """
        Redsi键名为all_user|(set)，存储所有的uid
        使用Redis的事物保证数据完整性
        使用Redis的管道保证命令执行的效率
        """
        data = list(set(data)) # 去除data列表中重复的值
        if not isinstance(data, list):
            # logging
            return 0

        # 过滤data中已经存在Redis中的数据，防止重复插入，浪费时间
        # sismembers复杂度是O(1)，sadd复杂度是O(n)
        # 这里好像没啥用，100条数据，查询100次是O(100)，插入也是O(100)
        # 先注释掉吧。。。。
        # for k in data:
        #     if self.r.sismembers(USER_SET, k) == 0：
        #         pass

        p = self.r.pipeline()
        try:
            for k in data:
                p.sadd(self.ALL_USER, k)
            result = p.execute()
        except:
            # logging
            return 0
        else:
            # logging
            return result

    def noCrawl(self, data):
        """
        存放未抓取的数据，key类型为set,
        data:
            type:list

        return list|int
        """

        # 如果是int类型，转换成list
        if isinstance(data, int):
            data = list(range(data, data+1))
        elif not isinstance(data, list):
            return 0

        data = list(set(data)) # 去除data列表中重复的值

        p = self.r.pipeline()

        try:
            for k in data:
                p.sadd(self.NO_CRAWL, k)
                p.sadd(self.ALL_USER, k) # 另存一份到ALL_USER表中
            result = p.execute()
        except:
            return 0
        else:
            return result

    def isCrawl(self, data):
        """
        存放所有已抓取过数据的uid,
        data：
            type: list|int

        return list|int
        """
        CRAWL = 'crawl'

        # 如果是int类型，转换成list
        if isinstance(data, int):
            data = list(range(data, data+1))
        elif not isinstance(data, list):
            return 0

        data = list(set(data))

        p = self.r.pipeline()
        try:
            for k in data:
                p.sadd(self.CRAWL, k)
            result = p.execute()
        except:
            return 0
        else:
            return result

    def spop(self):
        """
        当集合不为空时，弹出并返回key的一个随机元素
        """
        data = self.r.spop(self.NO_CRAWL)

        if data is None:
            return data
        else:
            return bytes.decode(data)

    def get_user(self, uid):
        tmp = self.r.hgetall(self.USER.format(uid=uid))
        user = dict()
        # 将字典中的key, value从bytes转换成str
        for k, v in tmp.items():
            k = bytes.decode(k)
            v = bytes.decode(v)
            user[k] = v
        return user

    def insert_user(self, info):
        """
        将用户信息存入数据库，
        info:
            type: dict
        result:
            成功返回True, 失败返回False
        """
        # print(info)
        # print(self.USER.format(uid=info['uid']))
        return self.r.hmset(self.USER.format(uid=info['uid']), info)




db = DB(host = 'localhost', port = 7000)
