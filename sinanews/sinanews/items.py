# -*- coding: utf-8 -*-


import scrapy


class SinanewsItem(scrapy.Item):

    # 获取所有一级栏目
    first_title = scrapy.Field()
    # 获取其url
    first_url = scrapy.Field()

    # 获取二级栏目
    first_child_title = scrapy.Field()
    # 栏目的url
    first_child_url = scrapy.Field()

    # 三级栏目
    first_grandchild_title = scrapy.Field()
    # 栏目url
    first_grandchild_url = scrapy.Field()

    # 文章内容
    content = scrapy.Field()
    # 文章标题
    title_head = scrapy.Field()
