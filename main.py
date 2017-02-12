#/usr/bin/env pyuthon
# coding=utf-8

from Db import db
from User import User
from Splider import splider

class Application(object):

    def crawl_uid(self):
        splider.crawl_uid()

    def crawl_info(self):
        while(True):
            splider.crawl_info()

    def run(self):
        self.crawl_uid()

        p = Pool(4)
        time5 = time.time()
        console.info("Process start.")
        for i in range(5):
            p.apply_async(self.crawl_info)
        p.close()
        p.join()
        time6 = time.time()
        console.info("Process end.")
        console.info("running {time}s".format(time=str(time6-time5)))

app = Application()
app.run()
# user = User(20484397)
# result = db.crawl(user.follow())
# print(result)

# print(user.follow())
