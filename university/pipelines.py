# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class UniversityPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if item['html']:
            if not self.collection.find_one({'url': item['url']}):
                self.collection.insert({'url': item['url'],
                                        'html': item['html'],
                                        'text': item['text'],
                                        'university': '四川大学'
                                        })
                print "===保存==="
                return item
        else:
            raise DropItem(u'没有数据 %s' % item)
