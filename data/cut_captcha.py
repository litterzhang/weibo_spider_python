#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'对验证码进行切割'

__author__='litterzhang'

import os
import random
from PIL import Image

# 绘制聚类分割结果
def draw_result(result, colors_num, x, y):
	im = Image.new('RGB', (x, y), color=(255, 255, 255))
	colors = [(random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)) \
		for i in range(colors_num)]
	for entry in result:
		im.putpixel([entry[0], entry[1]], colors[entry[2]])
	return im

# 加载图片
def get_im_from_file(fp):
	im = Image.open(fp)
	return im

def get_data_from_im(im):
	data = list()
	for j in range(im.size[1]):
		for i in range(im.size[0]):
			if im.getpixel((i, j))==0:
				data.append((i, j))
	return data

def get_data_from_file(fp):
	im = get_im_from_file(fp)
	data = get_data_from_im(im)
	return data

def cut_by_kmeans(data, k):
	iter_max = 10
	len_data = len(data)

	# 初始聚类中心点选取
	# cluster_centre = [data[i] for i in random.sample(range(len_data), k)]
	cluster_centre = [data[int(i*len_data/k)] for i in range(k)]

	cluster_mark = [-1 for x in range(len_data)]

	# 迭代iter_max次
	while True:
		# 对数据点选择cluster
		for i in range(len_data):
			# 计算第i个数据点的归属
			dis_min = 1000000000
			for p in range(k):
				dis = (data[i][0]-cluster_centre[p][0])**2 + \
						(data[i][1]-cluster_centre[p][1])**2

				if dis<dis_min:
					dis_min = dis
					cluster_mark[i] = p
		
		# 重新计算聚类中心
		cluster_centre_new = [[0, 0] for i in range(k)] 
		cluster_count = [0 for i in range(k)]
		for i in range(len_data):
			cluster_index = cluster_mark[i]
			cluster_centre_new[cluster_index][0] += data[i][0]
			cluster_centre_new[cluster_index][1] += data[i][1]
			cluster_count[cluster_index] += 1
		for i in range(k):
			if cluster_count[i]!=0:
				cluster_centre_new[i][0] /= cluster_count[i]
				cluster_centre_new[i][1] /= cluster_count[i]
			else:
				cluster_centre_new[i][0] = cluster_centre[i][0]
				cluster_centre_new[i][1] = cluster_centre[i][1]

		# 若聚类中心未改变，停止迭代
		change = False
		for i in range(k):
			if cluster_centre[i][0]!=cluster_centre_new[i][0] or \
				cluster_centre[i][1]!=cluster_centre_new[i][1]:
				change = True
				break
		if not change:
			break
		cluster_centre = cluster_centre_new

	return [(data[i][0], data[i][1], cluster_mark[i]) for i in range(len_data)]


if __name__=='__main__':
	input_dir = os.path.join(os.path.dirname(__file__), 'pre_img')
	output_dir = os.path.join(os.path.dirname(__file__), 'kmeans2_img')

	for filename in os.listdir(input_dir):
		filepath = os.path.join(input_dir, filename)

		im = get_im_from_file(filepath)
		data = get_data_from_im(im)

		result = cut_by_kmeans(data, 4)
		im = draw_result(result, 4, im.size[0], im.size[1])

		filepath_save = os.path.join(output_dir, 'kmeans_img_%s' % filename.split('_')[-1])
		im.save(filepath_save)
