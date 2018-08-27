# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	# 图片简介
	image_title = scrapy.Field()
	# 图片链接
	image_url = scrapy.Field()
	# 图片标签
	image_tag = scrapy.Field()
	# 图片缩略图链接
	image_thumb = scrapy.Field()

	# 定义mongodb数据库的集合和mysql的表名
	collection = table = 'images'

