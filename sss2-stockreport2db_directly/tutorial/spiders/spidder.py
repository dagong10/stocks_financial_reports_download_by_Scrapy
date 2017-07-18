# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import MySQLdb
import time
from ..items import StockItem
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

billnamelist = ["gdfx", "zcfzb", "lrb", "xjllb"]
check_stock = ["已退市", "停牌", "未上市", "基金资料"]
nrowsl = []
c = []


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # allowed_domains = ["dmoz.org"]


    def start_requests(self):
        urls = []
        conn = MySQLdb.connect(host='localhost', user='root', passwd='bbac2015', db='stocks',
                               port=3306, charset='utf8')
        cur = conn.cursor()
        cur.execute('select count(*) from stocklist')
        conn.commit()
        nrows = cur.fetchone()[0]
        nrowsl.append(nrows)
        c.append(0)
        cur.execute('select id from stocklist')
        conn.commit()
        numberlist = cur.fetchall()
        for i in range(0, nrows):  # nrows):  # range(nrows):,272)
            # number = sheetl.cell(i, 0).value
            i1 = i + 1
            number = numberlist[i][0]
            for j in range(len(billnamelist)):
                if billnamelist[j] == "gdfx":
                    url_str = "http://quotes.money.163.com/f10/" + str(billnamelist[j]) + "_" + str(number) + ".html"
                else:
                    url_str = "http://quotes.money.163.com/service/" + str(billnamelist[j]) + "_" + str(
                        number) + ".html?type=year"
                urls.append(url_str)
        cur.close()
        conn.close()
        for x in range(len(urls)):
            yield scrapy.Request(url=urls[x], callback=self.parse)

    def parse(self, response):
        sitem = StockItem()
        rl = response
        check = rl.text
        check_out = 0
        for checking in range(len(check_stock)):
            if check.find(check_stock[checking]) == -1:
                check_out += 1
        strrl = str(rl)
        rbillname = re.compile(r'[x z l g]\w*[b x]')  # f10/\w*_')
        rnumber = re.compile(r'\d{6}')
        if strrl.find("<200") != -1 and check_out == 4 and len(
                re.findall(rnumber, rl.url)) != 0:  # decide if the number is not direct to a valid stock info
            number = rnumber.findall(rl.url)[0]
            billname = rbillname.findall(rl.url)[0]
            sitem['rl'] = rl
            sitem['number'] = number
            sitem['billname'] = billname
            sitem['nrows'] = nrowsl[0]
            # cc+=1
            c[0] = (int(c[0]) + 1)
            sitem['counters'] = c[0]
            return sitem
