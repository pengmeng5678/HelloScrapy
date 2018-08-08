# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost",27017)
        db = client["dingdian"]
        self.Novel = db["novel"]

    def process_item(self, item, spider):
        try:
            self.Novel.insert(dict(item))
            print("保存到MongoDb成功")
        except Exception:
            print("保存到MongoDb失败")
        return item
