# _*_ coding:utf-8 _*_
# author: huhua


import requests
import re
import json
from requests.exceptions import RequestException
import time


def get_one_page(url):
	"""获取第一页"""
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
		response = requests.get(url, headers=headers) # 发送请求
		# 如果请求成功则返回内容
		if response.status_code == 200:
			return response.text
		else:
			return None
	except RequestException:
		return None


def parse_one_page(html):
	"""解析获取的页面"""
	# 正则提取内容依次为排名，图片链接，电影名，演员，上映时间(地区)
	# 创建正则对象
	pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>'
						 '.*?releasetime.*?>(.*?)</p>.*?</dd>', re.S)

	items = re.findall(pattern, html)
	for item in items:
		msg = {}
		msg['rank'] = item[0]
		msg['movie_name'] = item[2]
		msg['actors'] = item[3].strip()
		msg['time'] = item[4]
		msg['img'] = item[1]
		# 这里使用yield，每次遍历便生成一个字典数据，后面用for循环遍历
		yield msg


def save_to_txt(message):
	"""保存电影信息"""
	with open('movie_messages.txt', 'a', encoding='utf-8') as f:
		# write() argument must be str, not dict,不能直接写入，先用json转化一下
		f.write(json.dumps(message, ensure_ascii=False) + '\n')


def main(offset):
	# 目标url
	url = 'http://maoyan.com/board/4?offset=' + str(offset)
	# 获取第一页内容,这里需要定义一个函数取抓取网页
	html = get_one_page(url)
	# print(html)
	# 获取解析内容
	message = parse_one_page(html)
	# for i in message:
	# 	print(i)  测试
	# 保存解析内容
	for item in message:
		save_to_txt(item)


if __name__ == '__main__':
	for i in range(10):
		main(offset=i*10)
		time.sleep(1)






