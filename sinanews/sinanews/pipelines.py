# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinanewsPipeline(object):
    def process_item(self, item, spider):
        title = item['title_head']

        # 定义每个文件名
        fileName = title + ".txt"

        f = open(item['first_grandchild_title'] + '\\' + fileName, 'w')
        f.write(item['content'])
        f.close()

        return item
