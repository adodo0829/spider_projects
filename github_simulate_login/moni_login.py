# _*_ coding:utf-8 _*_
# author: huhua


import requests
from lxml import etree


class Login(object):
	"""创建模拟登陆Github类"""
	def __init__(self):
		"""初始化"""
		self.headers = {'Referer': 'https://github.com/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
			'Host': 'github.com'}
		self.login_url = 'https://github.com/login'
		self.post_url = 'https://github.com/session'
		self.logined_url = 'https://github.com/settings/profile'
		self.session = requests.Session()  # 维持会话，自动处理cookies

	def token(self):
		"""
		获取authenticity_token
		:return： token
		"""
		response = self.session.get(self.login_url, headers=self.headers)
		selector = etree.HTML(response.text)
		token = selector.xpath('//div//input[2]/@value')
		return token

	def login(self, email, password):
		"""开始模拟登陆，获取响应内容"""
		# 构建post表单
		post_data = {
			'commit': 'Sign in',
			'utf8': '✓',
			'authenticity_token': self.token()[0],
			'login': email,
			'password': password
		}
		response = self.session.post(self.post_url, data=post_data, headers=self.headers)
		if response.status_code == 200:
			self.dynamics(response.text)

		response = self.session.get(self.logined_url, headers=self.headers)
		if response.status_code == 200:
			self.profile(response.text)

	def dynamics(self, html):
		"""获取关注人的动态信息"""
		selector = etree.HTML(html)
		# 最近动态信息
		dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]')
		for item in dynamics:
			dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
			print(dynamic)

	def profile(self, html):
		"""获取关注人的账号信息"""
		selector = etree.HTML(html)
		# 昵称
		name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
		# 邮箱
		email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
		print(name, email)


if __name__ == "__main__":
	# 创建登陆对象
	login = Login()
	# 传入邮箱，密码
	login.login(email='appleguardu@163.com', password='password')
