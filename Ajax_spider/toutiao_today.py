# _*_ coding:utf-8 _*_
# author: huhua


import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool


headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'}

# 多进程抓取今日头条街拍图片
def get_page(offset):
	"""获取街拍页面"""
	# 页面为Ajax加载的，下面模拟Ajax请求，抓取页面
	params = {
		'offset': offset,
		'format': 'json',
		'keyword': '街拍',
		'autoload': 'true',
		'count': '20',
		'cur_tab': '1',
		'from': 'search_tab'
	}
	url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
	try:
		res = requests.get(url, headers=headers)
		if res.status_code == 200:
			return res.json()
	except requests.ConnectionError:
		return None


def get_images(json):
	"""获取每条数据中的图片链接，标题"""
	if json.get('data'):
		for item in json.get('data'):
			title = item.get('title')
			images = item.get('image_list')
			for image in images:
				yield {
					'title': title,
					'image': image.get('url')
				}


def save_image(item):
	"""保存下载图片"""
	if not os.path.exists(item.get('title')):
		os.mkdir(item.get('title'))
	try:
		response = requests.get('http:' + item.get('image'))
		if response.status_code == 200:
			file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
			if not os.path.exists(file_path):
				with open(file_path, 'wb') as f:
					f.write(response.content)
			else:
				print('Already Download', file_path)
	except requests.ConnectionError:
		print('Failed to Save Image')


def main(offset):
	"""街拍图片抓取"""
	json = get_page(offset)
	for item in get_images(json):
		print(item)
		save_image(item)


if __name__ == '__main__':
	# 使用多进程进行抓取
	GROUP_START = 1
	GROUP_END = 20
	pool = Pool()
	groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
	pool.map(main, groups)
	pool.close()
	pool.join()



