#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'合并抓取到的微博'

__author__='litterzhang'

import time
import json
import os

def combine():
	data_dir = os.path.join(os.path.dirname(__file__), 'data')
	weibos_hour_file = os.path.join(data_dir, 'weibos_hour_%s' % (str(int(time.time()))))
	weibos_all_file = os.path.join(data_dir, 'weibos_all')

	# 加载已经存储的微博ids
	weibos_old = []
	weibos_ids_old = []
	try:
		with open(weibos_all_file, 'r', encoding='utf-8') as fr:
			weibos_old = json.load(fr)
			for weibo in weibos_old:
				if weibo.get('id', None):
					weibos_ids_old.append(weibo['id'])
	except Exception as e:
		pass


	#读取当前时间段抓取的微博数据
	weibos_new = []
	weibos_ids_new = []
	for filename in os.listdir(data_dir):
		if filename.startswith('weibo_'):
			try:
				filepath = os.path.join(data_dir, filename)
				with open(filepath, 'r', encoding='utf-8') as fr:
					weibos_now = json.load(fr)

					for weibo in weibos_now:
						if weibo.get('id', None) and weibo['id'] not in weibos_ids_old and weibo['id'] not in weibos_ids_new:
							weibos_new.append(weibo)
							weibos_ids_new.append(weibo['id'])
				#删除当前文件
				os.remove(filepath)
			except Exception as e:
				pass

	#存储新抓取的微博
	with open(weibos_hour_file, 'w', encoding='utf-8') as fw:
		json.dump(weibos_new, fw, ensure_ascii=False)

	for weibo in weibos_new:
		weibos_old.append(weibo)

	with open(weibos_all_file, 'w', encoding='utf-8') as fw:
		json.dump(weibos_old, fw, ensure_ascii=False)

	print('weibo hour: %d' % len(weibos_new))
	print('weibo all: %d' % len(weibos_old))

def worker():
	while True:
		combine()
		time.sleep(3600)

if __name__=='__main__':
	worker()


