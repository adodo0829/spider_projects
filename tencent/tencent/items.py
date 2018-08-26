# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
	"""定义抓取内容"""
	# 职位名称
	jobName = scrapy.Field()
	# 职位详情描述
	jobDetail = scrapy.Field()
	# 职位类别
	jobType = scrapy.Field()
	# 职位需求人数
	jobNeed = scrapy.Field()
	# 工作地点
	jobLocation = scrapy.Field()
	# 招聘时间
	jobTime = scrapy.Field()

