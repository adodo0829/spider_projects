# _*_ coding:utf-8 _*_
# author: huhua


from selenium import webdriver
from urllib.parse import quote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from pymongo import MongoClient


# 创建数据库
client = MongoClient(host='localhost', port=27017)
db = client.taobao_iphone
collection = db.Iphone

# Headless模式
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

keyword = 'iphone'
web_wait = WebDriverWait(browser, 10)


def page_get(page):
	"""抓取商品列表页
	:param page：页码数
	"""
	print('正在抓取第%d页...'%page)
	url = 'https://s.taobao.com/search?q=' + quote(keyword) # 构造URL
	try:
		browser.get(url)
		# 翻页操作
		if page > 1:
			# 获取页码输入框
			page_input = web_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
			# 获取“确定”按钮
			page_submit = web_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
			# 清空输入框，输入page，点击确定
			page_input.clear()
			page_input.send_keys(page)
			page_submit.click()
		# 确定跳转页是否是高丽页
		web_wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
		# 加载页面，这里使用显式等待,指定等待条件：等待指定元素(每个商品的信息item)加载出来
		web_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
		# 获取页面源代码
		html = browser.page_source
		return html
	except TimeoutException:
		# 若页面超时，继续获取
		page_get(page)


def page_parse(html):
	"""解析页面，提取商品数据"""
	# 商品图片，价格，成交量，店铺标题，店铺名，店铺地点
	doc = pq(html)
	# 提取所有商品信息
	items = doc('#mainsrp-itemlist .items .item').items()
	for item in items:
		# 用一个字典来保存每件商品的数据
		product = {
			'image': item.find('.pic .img').attr('data-src'),
			'price': item.find('.price').text().replace('\n', ''),
			'deal': item.find('.deal-cnt').text(),
			'title': item.find('.title').text().replace('\n', ''),
			'shop': item.find('.shop').text(),
			'location': item.find('.location').text()
		}
		yield product


def data_save(msg):
	"""保存商品数据"""
	try:
		if collection.insert(msg):
			print('save to mogon successfully!')
	except Exception:
		print('fail to save')


def main():
	"""主控制"""
	# 1.拿到页面
	# 2.解析页面
	# 3.保存数据
	# 4.遍历所有页面,拿到所有数据
	max_page = 100
	for i in range(1, max_page+1):
		html = page_get(i)
		msg = page_parse(html)
		# print(msg)
		data_save(msg)
	browser.close()


if __name__ == "__main__":
	main()

