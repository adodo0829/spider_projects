# _*_ coding:utf-8 _*_
# author: huhua


import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import time
from pymongo import MongoClient


# 将数据存入数据库
client = MongoClient(host='localhost', port=27017)
db = client.News
collection = db.basa_news


# 构造请求头，直接从Request Headers里面复制过来
headers = {
	'Referer': 'https://m.weibo.cn/u/1990303727',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest'
}

def get_page(page):
	"""获取页面内容"""
	# url里包含参数，需构造参数字典,其中page为变量
	params = {
		'type': 'uid',
	    'value': '1990303727',
	    'containerid': '1076031990303727',
	    'page': page
	}
	# https://m.weibo.cn/api/container/getIndex?type=uid&value=1990303727&containerid=1076031990303727&page=2
	url = 'https://m.weibo.cn/api/container/getIndex?' + urlencode(params) # 参数需要转化为上述形式
	try: # 异常处理
		response = requests.get(url, headers=headers)
		if response.status_code == 200: # 连接成功
			# print(response.json())
			return response.json()
	except requests.RequestException as e:
		print('Error:', e.args)


def parse_page(res):
	"""解析文本，提取内容"""
	if res:
		items = res.get('data').get('cards')
		for item in items:
			msg = item.get('mblog')
			# 找个字典存放数据
			info = {}
			# 因为文本数据中含有HTML标签，导入pyquery进行处理
			info['text'] = pq(msg.get('text')).text()
			info['attitude'] = msg.get('attitudes_count')
			info['comment'] = msg.get('comments_count')
			info['repost'] = msg.get('reposts_count')
			yield info


def save_to_mongo(result):
	"""将字典数据存入MongoDB"""
	# 由于是字典数据，不需要进行处理
	if collection.insert(result):
		print('Save Successfully')


if __name__ == "__main__":

	# get_page(2) 测试，原始页面中第一页page没有值,需做特殊处理
	# page = 2
	for page in range(2, 20):
		res = get_page(page)
		results = parse_page(res)
		for result in results:
			print(result)
			time.sleep(1)
			save_to_mongo(result)










