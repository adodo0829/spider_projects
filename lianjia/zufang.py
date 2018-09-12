# _*_ coding:utf-8 _*_
# author: huhua


import re
import time
import requests
from lxml.html import etree


class LianJiaZuFang(object):
	"""获取深圳地区链家网租房信息"""
	def __init__(self):
		'''初始化一些信息'''
		self.url = 'https://sz.lianjia.com/zufang/'
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
			              'Chrome/69.0.3497.81 Safari/537.36',
			'Host': 'sz.lianjia.com',
			}

	# 获取深圳各区域url链接
	def get_area_link(self):
		try:
			response = requests.get(self.url, headers=self.headers)
			if response.status_code == 200:
				content = etree.HTML(response.text)
				links = content.xpath('//*[@id="filter-options"]/dl[1]/dd/div/a/@href')[1:]
				areas = content.xpath('//*[@id="filter-options"]/dl[1]/dd/div[1]/a/text()')[1:]
				print(areas)
				# print(links)
				for i in range(len(areas)):
					area = areas[i]
					link = self.url + links[i][8:]
					self.get_area_page(area, link)
		except:
			print('请求出现错误！')

	# 获取各区域总页面数，拼接出每一页的url
	def get_area_page(self, area, url):
		try:
			response = requests.get(url, headers=self.headers)
			pages = int(re.findall("page-data='{\"totalPage\":(\d+),\"curPage\":1}", response.text)[0])
			print('这个区域有%s页'%pages)
			for page in range(1, pages+1):
				info_url = url + 'pg' + str(page)
				print('正在抓取第%d页'%page)
				# time.sleep(random.random())
				self.get_house_info(area, info_url)
		except:
			print('局部请求错误！')

	# 获取每一页的详细租房信息
	def get_house_info(self, area, info_url):
		print('开始抓取该页信息')
		time.sleep(5)
		try:
			response = requests.get(info_url, headers=self.headers)
			# if response.status_code == 200:
			content = etree.HTML(response.text)
			#每个页面的信息条数
			num = len(content.xpath('//*[@id="house-lst"]/li/@data-index'))
			print('本页面有%d条租房信息'%num)
			time.sleep(1)
			for i in range(num):
				# 房屋简述
				description = content.xpath('//*[@id="house-lst"]/li/div[2]/h2/a/text()')[i]
				# 房屋所在小区
				location = content.xpath('//*[@id="house-lst"]/li/div[2]/div[1]/div[1]/a/span/text()')[i]
				# 房型
				house_type = content.xpath('//*[@id="house-lst"]/li/div[2]/div[1]/div[1]/span[1]/span/text()')[i]
				# 面积大小
				size = content.xpath('//*[@id="house-lst"]/li/div[2]/div[1]/div[1]/span[2]/text()')[i]
				b_size = re.findall(r'(.*)平米', size)[0]
				# 房屋朝向
				orientation = content.xpath('//*[@id="house-lst"]/li/div[2]/div[1]/div[1]/span[3]/text()')[i]
				# 层高
				floor = re.findall('(\d+)', content.xpath('//*[@id="house-lst"]/li/div[2]/div[1]/div[2]/div/text()[1]')[i])[0]
				# 房屋年份
				try:
					year = re.findall('(\d+)', content.xpath('//*[@id="house-lst"]/li/div[2]/div[1]/div[2]/div/text()[2]')[i])[0]
				except Exception as e:
					year = ''
				# 租金
				price = content.xpath('//*[@id="house-lst"]/li/div[2]/div[2]/div[1]/span/text()')[i]

				print(area, location, house_type, size, b_size, orientation, floor, year, price, description)
				# 写入本地文件
				with open('F:\spider_projects\Ajax_Spider\SZLJ.txt', 'a', encoding='utf-8') as f:
					f.write(area +',' + location +',' + house_type +',' + size +',' + b_size +',' + price +',' + floor +',' +'朝向:' + orientation +',' + year +',' + description + '\n')
					print('已写入该页内容')

		except Exception as e:
			print('信息获取失败！重新尝试获取本页信息。。。')
			time.sleep(5)
			return self.get_house_info(area, info_url)


	def start(self):
		self.get_area_link()


if __name__ == "__main__":
		lj = LianJiaZuFang()
		lj.start()













