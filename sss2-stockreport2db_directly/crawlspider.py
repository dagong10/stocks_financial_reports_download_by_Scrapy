# coding:utf-8

from scrapy import cmdline
import time

t1=time.time()

cmdline.execute("scrapy crawl quotes".split())

t2=time.time()
print "time_cost=%s"%(t2-t1)