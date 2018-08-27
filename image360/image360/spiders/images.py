# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from image360.items import ImageItem
import json


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        """生成请求"""
        # 构造url参数
        data = {'ch': 'home', 't1': 592, 'listtype': 'new', 'temp': 1}
        # 初始url
        base_url = 'http://image.so.com/zj?'
        # 生成request请求,在setting文件中设置想爬取的页数，每页是30张图
        for page in range(1, self.settings.get('MAX_PAGE')+1):
            data['sn'] = page*30 # 动态的sn参数，偏移量
            params = urlencode(data) # 字典参数转化为URL参数
            url = base_url + params
            # 生成Request
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """处理响应的json数据"""
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['image_title'] = image.get('group_title')
            item['image_url'] = image.get('qhimg_url')
            item['image_tag'] = image.get('tag')
            item['image_thumb'] = image.get('qhimg_thumb_url')
            yield item

