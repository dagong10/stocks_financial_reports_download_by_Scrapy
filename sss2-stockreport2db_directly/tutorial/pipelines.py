# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import bs4
from bs4 import BeautifulSoup
import re
import time
import MySQLdb
import sys
import os
import codecs

reload(sys)
sys.setdefaultencoding("utf-8")
billnamelist = ["zcfzb", "lrb", "xjllb"]


class TutorialPipeline(object):
    def process_item(self, item, spider):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='bbac2015', db='stocks',
                               port=3306, charset='utf8')
        cur = conn.cursor()
        nrows = item['nrows']
        rl = item['rl']
        number = item['number']
        billname = item['billname']
        counters = item['counters']
        print counters,
        print "/%s"%(int(nrows)*4)
        table_name = '_' + number
        soupl = BeautifulSoup(rl.text, 'html.parser')
        content = rl.text
        if billname == "gdfx":
            save_stock_amount(conn, cur, number, billname, soupl)
        else:
            print billname
            cvst = content.split('\r\n')
            ncols = len(cvst[0].split(',')) - 1
            #t = time.time()
            save_2_stocklist(conn, cur, number, billname, ncols, content)
            #t1 = time.time()
            #print 'save_2_stocklist=%s s' % (t1 - t)
            #------------------set the refill table work in EV to save time----------------------------
            '''cur.execute("select lrb_ncols,xjllb_ncols,zcfzb_ncols from stocklist where id='%s'" % number)
            conn.commit
            nncols = cur.fetchone()  # 获得所有表格分别的列数
            if nncols.count(0) == 0:  # 如果都已经读完，没有0列的表
                cur.execute("DROP TABLE IF EXISTS %s" % table_name)
                conn.commit()
                #t2 = time.time()
                ncols = min(nncols)  # 去最少表列
                set_date_column(conn, cur, cvst[0], table_name, ncols)
                #t3 = time.time()
                #print "set_data_column_cost=%s s" % (t3 - t2)
                for i in range(len(billnamelist)):
                    billname = billnamelist[i]
                    value = (billname + '_data', number)
                    cur.execute("select %s from stocklist where id=%s" % value)
                    conn.commit
                    data = cur.fetchone()[0]
                    fill_data(conn, cur, table_name, ncols, data)
                #t4 = time.time()
                #print 'fill_data_total_cost=%s s' % (t4 - t3)'''
        cur.close()
        conn.close()
        return item


def save_stock_amount(conn, cur, number, billname, soupl):  # 保存股本数
    loc0 = soupl.find(class_="table_bg001 border_box")  # 找到表格
    loc1 = loc0.find_all("td")  # 找到所有行
    loc2 = loc1[1]  # 找到第2行
    stock_amount = int(float(loc2.string) * 10000)
    stock_link = "http://quotes.money.163.com/1" + number + ".html"
    value = (stock_amount, stock_link, number)
    print value
    print "amount=%s" % stock_amount
    cur.execute("update stocklist set amount_10000=%d,stock_link='%s'  where id='%s' " % value)
    conn.commit()
    return


def save_2_stocklist(conn, cur, number, billname, ncols, content):#save report content to mysqldb
    value = (str(billname + '_ncols'), ncols, str(billname + '_data'), content, number)
    cur.execute("update stocklist set %s=%d,%s='%s' where id='%s'" % value)
    conn.commit()
    return

'''
def set_date_column(conn, cur, cvst0, table_name, ncols):
    cvst1 = cvst0.replace('-', '_')
    rda = cvst1.split(',')[:ncols]
    sqls = "CREATE TABLE IF NOT EXISTS %s(item CHAR(100)"
    for i in range(1, ncols):
        sqls += "," + rda[i] + " " + 'float(11)'
    sql = sqls + ')'
    cur.execute(sql % table_name)
    conn.commit()
    return


def fill_data(conn, cur, table_name, ncols, data):
    filename = "C:\ProgramData\MySQL\Uploads\middle.csv"
    if os.path.exists(filename):
        os.remove("C:\ProgramData\MySQL\Uploads\middle.csv")
    fp = codecs.open(filename, "w", "UTF-8")
    fp.write(data)
    fp.close
    sql = "LOAD DATA local INFILE 'C:/ProgramData/MySQL/Uploads/middle.csv' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES"
    cur.execute(sql % table_name)
    conn.commit()
    return
'''