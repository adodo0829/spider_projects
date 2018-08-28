# -*- coding: utf-8 -*-
import scrapy
from sinanews.items import SinanewsItem
import os


class SinanewSpider(scrapy.Spider):
	name = 'sinanew'
	allowed_domains = ['news.sina.com.cn']
	start_urls = ['http://news.sina.com.cn/guide']

	def parse(self, response):
		"""处理一级栏目返回的response"""
		items = []

		# 一级栏目名称&url的list集合
		first_title = response.xpath('//*[@id="tab01"]/div/h3/a/text()').extract()
		first_url = response.xpath('//*[@id="tab01"]/div/h3/a/@href').extract()

		# 二级栏目标题集合,url
		first_child_title = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()
		first_child_url = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()

		# 创建本地文件一级目录
		for i in range(0, len(first_title)):
			# 创建文件夹名
			file_name1 = '.\新浪资讯\\' + first_title[i]
			if not os.path.exists(file_name1):
				os.makedirs(file_name1)

			# 处理item
			for j in range(0, len(first_child_url)):
				# 初始化item对象
				item = SinanewsItem()

				# 先保存一级栏目的title和url
				item['first_title'] = first_title[i]
				item['first_url'] = first_url[i]

				# 处理二级栏目，并将栏目文件存放在上一目录中
				# 判断二级栏目url的开头是以主栏目,如果是，则创建子目录
				belong = first_child_url[j].startswith(item['first_url'])
				if belong:
					file_name11 = file_name1 + '\\' + first_child_title[j]
					if not os.path.exists(file_name11):
						os.makedirs(file_name11)
					# 保存二级目录的title， url
					item['first_child_title'] = first_child_title[j]
					item['first_child_url'] = first_child_url[j]
					item['first_grandchild_title'] = file_name11

					# 将item保存但集合中，方便到子栏目的解析方法中使用
					items.append(item)

		# 发送二级栏目url的Request请求，得到Response连同包含meta数据 一同交给回调函数 second_parse方法
		for item in items:
			yield scrapy.Request(url=item['first_child_url'], meta={'meta_1': item}, callback=self.second_parse)


	def second_parse(self, response):
		"""处理二级栏目返回的response"""
		items = []

		# 提取Response中的meta数据
		meta_1 = response.meta['meta_1']

		# 提取出下一栏目的url
		first_grandchild_url = response.xpath('//ul/li/a/@href').extract()

		for i in range(0, len(first_grandchild_url)):
			# 筛选出了属于上一级链接下的子url
			belong = first_grandchild_url[i].endswith('.shtml') and first_grandchild_url[i].startswith(meta_1['first_url'])
			# 如果属于上级栏目，则放在同一个item下
			if belong:
				item = SinanewsItem()
				item['first_title'] = meta_1['first_title']
				item['first_url'] = meta_1['first_url']
				item['first_child_title'] = meta_1['first_child_title']
				item['first_child_url'] = meta_1['first_child_url']
				item['first_grandchild_title'] = meta_1['first_grandchild_title']
				# 三级目录链接
				item['first_grandchild_url'] = first_grandchild_url[i]

				# 将item保存但集合中，方便到下一链接的解析方法中使用
				items.append(item)

		# 发送每个二级目录下子链接url的Request请求，得到Response后连同包含meta数据 一同交给回调函数 detail_parse 方法处理
		for item in items:
			yield scrapy.Request(url=item['first_grandchild_url'], meta={'meta_2': item}, callback=self.detail_parse)

	def detail_parse(self, response):
		"""解析详情页，含有数据文本的网页"""
		item = response.meta['meta_2']
		# 文章标题
		title_head = response.xpath('//*[@id="article"]/p[1]/text()').extract_first()
		# 文章内容，包含在所有P标签中
		contents = response.xpath('//*[@id="article"]/p/text()').extract()

		content = ""
		# 合并p标签内容
		for con in contents:
			content += con
		# 去除空格等
		content = "".join(content.split())

		item['title_head'] = title_head
		item['content'] = content
		yield item









