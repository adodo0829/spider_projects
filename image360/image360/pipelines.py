# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem


class MongoPipeline(object):
	"""保存数据到mongodb"""
	def __init__(self, mongo_user, mongo_db):
		# 初始化数据库,用户名，数据库名
		self.mongo_user = mongo_user
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		# 获取setting文件的mongo配置信息
		return cls(
			mongo_user=crawler.settings.get('MONGO_USER'),
			mongo_db=crawler.settings.get('MONGO_DB')
		)

	def open_spider(self, spider):
		"""链接数据库"""
		self.client = pymongo.MongoClient(self.mongo_user)
		# 指定数据库
		self.db = self.client[self.mongo_db]

	def process_item(self, item, spider):
		"""处理数据，出入数据库"""
		self.db[item.collection].insert(dict(item))
		return item

	def close_spider(self, spider):
		"""关闭数据库链接"""
		self.client.close()


class MysqlPipeline(object):
	"""保存数据到MySQL"""
	def __init__(self, host, port, user, password, database):
		# 初始化数据库信息
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.database = database

	@classmethod
	def from_crawler(cls, crawler):
		# 从setting获取mysql配置
		return cls(
			host=crawler.settings.get('MYSQL_HOST'),
			port=crawler.settings.get('MYSQL_PORT'),
			user=crawler.settings.get('MYSQL_USER'),
			password=crawler.settings.get('MYSQL_PASSWORD'),
			database=crawler.settings.get('MYSQL_DB'),
		)

	def open_spider(self, spider):
		"""建立连接mysql"""
		self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
		self.cursor = self.db.cursor()

	def close_spider(self, spider):
		"""断开链接mysql"""
		self.db.close()
		# pass

	def process_item(self, item, spider):
		"""保存数据至mysql"""
		# 将item字典化
		data = dict(item)
		keys = ', '.join(data.keys()) # 获取插入mysql的列的值
		values = ', '.join(['%s'] * len(data)) # 构造插入值的占位符
		# 构造动态的SQL语句
		sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=item.table, keys=keys, values=values)
		try:
			if self.cursor.execute(sql, tuple(data.values())):
				self.db.commit()
		except:
			self.db.rollback()
		return item


class ImagePipeline(ImagesPipeline):
	"""继承ImagePipeline类，处理图片"""

	def file_path(self, request, response=None, info=None):
		url = request.url # 图片链接
		file_name = url.split('/')[-1] # 取链接/最后一部分作为文件名
		return file_name

	def item_completed(self, results, item, info):
		"""遍历下载列表"""
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
			raise DropItem('image download failed')
		return item

	def get_media_requests(self, item, info):
		"""生成Item爬取对象"""
		yield Request(item['image_url'])












