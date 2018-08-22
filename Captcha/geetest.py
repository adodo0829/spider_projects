# _*_ coding:utf-8 _*_
# author: huhua


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from io import BytesIO
from PIL import Image
import random
from selenium.webdriver import ActionChains



browser = webdriver.Chrome()
browser.maximize_window()
browser.get('https://account.geetest.com/login')
wait = WebDriverWait(browser, 15)


def get_click_button():
	"""
	输入账号密码，获取点击按钮
	:return: click_button
	"""
	# 获取账号，密码输入框
	email = wait.until(EC.presence_of_element_located((By.ID, 'email')))
	password = wait.until(EC.presence_of_element_located((By.ID, 'password')))
	# 输入账号，密码
	email.send_keys('appleguardu@163.com')
	password.send_keys('hh0127')
	time.sleep(2)
	# 获取点击按钮
	click_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
	return click_button


def get_screenshot():
	"""
	获取网页截图
	:return: 截图对象
	"""
	screenshot = browser.get_screenshot_as_png()
	screenshot = Image.open(BytesIO(screenshot))
	# print(screenshot)
	return screenshot


def get_captcha_position(pos):
	"""
	获取验证码位置
	:return: 验证码位置参数
	"""
	img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, pos)))
	time.sleep(2)
	location = img.location
	size = img.size
	top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
	return (top, bottom, left, right)


def get_unFull_captcha(name):
	"""
	获取带缺口验证码图片
	:return: unfull captcha
	"""
	top, bottom, left, right = get_captcha_position('geetest_canvas_slice')
	print('验证码1位置:', top, bottom, left, right)
	screenshot = get_screenshot()
	unfull_captcha = screenshot.crop((left, top, right, bottom)) # 按图片位置裁剪
	unfull_captcha.save(name)     # 这里传入的name要以xxx.png命名
	return unfull_captcha


def get_full_captcha(name):
	"""
	获取完整验证码图片
	:return: full_captcha
	"""
	# 这里要执行JavaScript脚本才能拿到完整图片的截图
	show_Full_img1= "document.getElementsByClassName('geetest_canvas_fullbg')[0].style.display='block'"
	browser.execute_script(show_Full_img1)
	show_Full_img2 = "document.getElementsByClassName('geetest_canvas_fullbg')[0].style.opacity=1"
	browser.execute_script(show_Full_img2)
	# 等待完整图片加载
	time.sleep(2)
	top, bottom, left, right = get_captcha_position('geetest_canvas_fullbg')
	print('验证码2位置:', top, bottom, left, right)
	screenshot = get_screenshot()
	full_captcha = screenshot.crop((left, top, right, bottom))  # 同上
	full_captcha.save(name)
	return full_captcha


def get_quekou_distance(image1, image2):
	"""
	对比像素点，获取缺口位置
	:param image1: 缺口图片
	:param image2: 完整图片
	:return: 缺口的偏移距离
	"""
	# 缺口在滑块右侧，设定遍历初始横坐标left为59
	left = 60
	# 像素对比阈值
	threshold = 60

	for i in range(left, image2.size[0]):
		for j in range(image2.size[1]):
			rgb1 = image1.load()[i, j]
			rgb2 = image2.load()[i, j]

			res1 = abs(rgb2[0] - rgb1[0])
			res2 = abs(rgb2[1] - rgb1[1])
			res3 = abs(rgb2[2] - rgb1[2])
			if not (res1 < threshold and res2 < threshold and res3 < threshold):
				return i-7 # 返回缺口偏移距离，这里需测试几次


def get_track(distance):
	"""
	获取移动路径
	:param distance: 偏移量
	:return: track：移动轨迹
	"""
	# 存放移动轨迹
	track = []
	# 当前位置
	current = 0
	# 设定加速段和减速段临界点为路径的3/4处
	mid = distance*4/5
	# 时间间隔time, 取0.2~0.3之间随机数，避免被网站识别出来
	t = random.randint(2, 3)/10
	# 初速度
	v = 0

	while current < distance:
		if current < mid:
			# 匀加速移动，加速度a
			a = 2
		else:
			a = -3
		# 初速度
		v0 = v
		# 当前速度
		v = v0 + a*t
		# 移动距离
		s = v0*t + 1/2 * a * t*t
		# 当前位移
		current += s
		# 加入到移动轨迹
		track.append(round(s))
	return track


def move(slider, track):
	"""
	模拟鼠标操作，点击，移动滑块按钮
	:param: 滑块
	:param: 轨迹
	:return:
	"""
	ActionChains(browser).click_and_hold(slider).perform()
	# 操作鼠标按轨迹移动
	for x in track:
		ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
	time.sleep(0.3)
	# 松开
	ActionChains(browser).release().perform()


def get_slider():
	"""获取滑块
	:return: 滑块对象
	"""
	slider = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
	return slider


def login():
	"""
	点击登陆
	:return:
	"""
	submit = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
	submit.click()
	time.sleep(10)
	print('登录成功')


def main():
	"""主函数"""

	# 获取带缺口验证码图片image1, 传入的参数后缀为： .png
	image1 = get_unFull_captcha('unfull_captcha.png')
	# print(image1.load()[12,25])
	# 获取完整验证码图片image2
	image2 = get_full_captcha('full_captcha.png')
	# 对比上述图片像素点，获取缺口位置，得到偏移距离
	distance = get_quekou_distance(image1, image2)
	print('缺口偏移量:', distance)
	# 获取滑块的移动轨迹
	track = get_track(distance)
	# 模拟人的行为，拖动滑块，完成验证
	slider = get_slider()
	move(slider, track)
	success = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
	print(success)
	if success:
		login()
	else:
		main()

if __name__ == '__main__':
	# 登陆账号，密码,获取点击按钮，模拟点击
	get_click_button().click()
	main()


