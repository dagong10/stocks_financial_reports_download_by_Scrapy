# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field
    rl=scrapy.Field()
    number=scrapy.Field()
    billname=scrapy.Field()
    nrows=scrapy.Field()
    counters=scrapy.Field()
    pass
