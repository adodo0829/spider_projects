# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class TencentpositionSpider(scrapy.Spider):
	name = 'tencent'
	allowed_domains = ['hr.tencent.com']
	# 定义初始URL
	url = 'https://hr.tencent.com/position.php?&start='
	# 初始偏移量
	offset = 0
	start_urls = [url + str(offset)]

	def parse(self, response):
		"""处理response"""
		for eachJob in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
			# 初始化item对象
			item = TencentItem()
			# 将一页的内容放入item中
			item['jobName'] = eachJob.xpath('./td[1]/a/text()').extract()[0]

			item['jobDetail'] = eachJob.xpath('./td[1]/a/@href').extract()[0]
			item['jobType'] = eachJob.xpath('./td[2]/text()').extract_first()
			item['jobNeed'] = eachJob.xpath('./td[3]/text()').extract()[0]
			item['jobLocation'] = eachJob.xpath('./td[4]/text()').extract()[0]
			item['jobTime'] = eachJob.xpath('./td[5]/text()').extract()[0]
			# 将获取的数据交给pipeline
			yield item

		# 提取出接下来的请求,每页10条
		if self.offset < 3300:
			self.offset += 10
		else:
			print('the work finished')
		next_page = self.url + str(self.offset)

		# 将请求重新发送给调度器入队列，出队列，给下载器下载
		yield scrapy.Request(url=next_page, callback=self.parse)
























