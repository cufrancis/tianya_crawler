#!/usr/bin/env python
# coding=utf-8

import curses

class Console(object):

    HEADER = '\033[95m'
    INFO = '\033[0;47;40m' # 白色
    OKBLUE = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'

    def __init__(self):
        # import curses
        pass

    def open(self):
        """
        开始输出
        """
        pass

    def process(self):
        """
        输出进度条
        """
        pass

    def info(self, msg, close=True):
        """
        普通文本
        白色
        """
        print("{info}{msg}".format(info=self.INFO, msg=msg),end='')
        if close:
            self.close()

    def success(self, msg, close=True):
        """
        显示成功信息
        信息为绿色
        """
        print("{success}{msg}".format(success=self.SUCCESS, msg=msg),end='')
        if close:
            self.close()

    def error(self, msg, close=True):
        """
        错误警报
        信息为红色
        """
        print("{error}{msg}".format(error=self.ERROR, msg=msg),end='')
        if close:
            self.close()

    def close(self):
        print("\r")
        pass

console = Console()
