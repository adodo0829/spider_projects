# _*_ coding:utf-8 _*_
# author: huhua


import pandas as pd
import numpy as np
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

# 设置图形的样式
plt.style.use("fivethirtyeight")
# 中文显示
sns.set_style({'font.sans-serif':['simhei','Arial']})


f = open('F:\spider_projects\Ajax_Spider\SZLJ.txt', 'r', encoding='utf-8')

lj_df = pd.read_csv(f, sep=',', header=None, encoding='utf-8', names=['area', 'location', 'house_type', 'size', 'b_size', 'price',
                                                                 'floor', 'direction', 'house_year', 'describe'])
# 添加新特征值
df = lj_df.copy()
df['per_price'] = lj_df['price']/lj_df['b_size']

# 从新排出列位置
columns = ['area', 'location', 'house_type', 'b_size', 'price', 'per_price', 'floor', 'direction', 'house_year']
df = pd.DataFrame(df, columns=columns)
# 重新查看一下数据集
# print(df.info())
# print(df.describe())

# 对于区域特征area，我们可以分析不同区域每平米租金和数量的对比。
# 按区域分组对比数量和价格
def area_analyze():
	df_house_count = df.groupby('area')['price'].count().sort_values(ascending=False).to_frame().reset_index()
	df_house_mean = df.groupby('area')['per_price'].mean().sort_values(ascending=False).to_frame().reset_index()

	# 作图
	f, [ax1, ax2, ax3] = plt.subplots(3,1,figsize=(20,15))
	sns.barplot(x='area', y='per_price', palette="Blues_d", data=df_house_mean, ax=ax1)
	ax1.set_title('深圳各区房租每平米单价对比',fontsize=15)
	ax1.set_xlabel('区域')
	ax1.set_ylabel('每平米单价')

	sns.barplot(x='area', y='price', palette="Greens_d", data=df_house_count, ax=ax2)
	ax2.set_title('深圳各区出租房数量对比',fontsize=15)
	ax2.set_xlabel('区域')
	ax2.set_ylabel('数量')

	sns.boxplot(x='area', y='price', data=df, ax=ax3)
	ax3.set_title('深圳各区房租总价',fontsize=15)
	ax3.set_xlabel('区域')
	ax3.set_ylabel('房租总价')

	plt.show()

# 对面积特征size的分析
def size_analyze():
	# 作图
	f, [ax1, ax2] = plt.subplots(1, 2, figsize=(15, 5))
	# 建房时间的分布情况
	sns.distplot(df['b_size'], bins=20, ax=ax1, color='r')
	sns.kdeplot(df['b_size'], shade=True, ax=ax1)
	# 建房时间和出租价格的关系
	sns.regplot(x='b_size', y='price', data=df, ax=ax2)

	plt.show()

# 对户型进行分析
def type_analyze():
	f, ax1 = plt.subplots(figsize=(20, 20))
	sns.countplot(y='house_type', data=df, ax=ax1)
	ax1.set_title('房屋户型', fontsize=15)
	ax1.set_xlabel('数量')
	ax1.set_ylabel('户型')
	plt.show()

# 根据散点图发现异常数据，进行剔除
# r = df.loc[df['b_size']> 400]
# print(r)
df = df[(df['location']!='新天鹅堡')&(df['b_size']<400)]

# area_analyze()
# size_analyze()
# size_analyze()
# type_analyze()