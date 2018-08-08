# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #小说的名字
    name = scrapy.Field()
    #作者
    author = scrapy.Field()
    #小说地址
    novelurl = scrapy.Field()
    #状态
    serialstatus = scrapy.Field()
    #连载字数
    serialnumber = scrapy.Field()
    #文章类别
    category = scrapy.Field()


