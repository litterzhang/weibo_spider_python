#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'将获取的数据分词，变成一条条记录'

__author__='litterzhang'

import os
import json
import time

import jieba
jieba.load_userdict('dict.txt')
import jieba.posseg as pseg

#加载users表
def load_users(fp):
	users = list()
	with open(fp, 'r', encoding='utf-8') as fr:
		for line in fr:
			try:
				user = json.loads(line)
				users.append(user)
			except Exception as e:
				print('加载users出错: %s' % e)
	return users

#存储users
def dump_users(fp, users):
	with open(fp, 'w', encoding='utf-8') as fw:
		for user in users:
			user_json = json.dumps(user, ensure_ascii=False)
			fw.write(user_json + '\n')

#存储weibo记录
def dump_records(records):
	records_hour_file = os.path.join(os.path.dirname(__file__), \
		'result/records_hour_%s' % (str(int(time.time()))))
	records_all_file = os.path.join(os.path.dirname(__file__), \
		'result/records_all')

	try:
		records_hour = open(records_hour_file, 'w', encoding='utf-8')
		records_all = open(records_all_file, 'a', encoding='utf-8')

		for record in records:
			record_json = json.dumps(record, ensure_ascii=False)
			records_all.write(record_json + '\n')
			records_hour.write(record_json + '\n')
	except Exception as e:
		print('存储weibo记录出错: %s' % e)
	finally:
		if records_all:
			records_all.close()
		if records_hour:
			records_hour.close()
	return records_hour_file

# 存储texts
def dump_texts(texts):
	texts_all_file = os.path.join(os.path.dirname(__file__), \
		'result/texts')
	texts_hour_file = os.path.join(os.path.dirname(__file__), \
		'result/texts_hour_%s' % (str(int(time.time()))))

	try:
		texts_hour = open(texts_hour_file, 'w', encoding='utf-8')
		texts_all = open(texts_all_file, 'a', encoding='utf-8')

		for text in texts:
			text_for_w = ' '.join([x[0] for x in text])
			texts_hour.write(text_for_w + '\n')
			texts_all.write(text_for_w + '\n')
	except Exception as e:
		print('存储分词结果出错: %s' % e)
	finally:
		if texts_all:
			texts_all.close()
		if texts_hour:
			texts_hour.close()
	return texts_hour_file

#切割句子
def cut_sentence(str):
	fiter_flag = list(['p', 'eng', 'x', 'uj', 'm', 'u', 'c', 'r'])
	result = pseg.cut(str)
	result = filter(lambda x: x.flag not in fiter_flag, result)
	result = filter(lambda x: len(x.word)>1, result)

	return list([(x.word, x.flag) for x in result])

#处理json文件
def cut_json_file(filepath):
	users = load_users(os.path.join(os.path.dirname(__file__), 'result/users'))
	records = list()
	texts = list()

	try:
		with open(filepath, 'r', encoding='utf-8') as fr:
			data_list = json.load(fr)

			for data in data_list:
				user = data.get('user', None)
				record = dict(data)

				#处理user
				if user:
					record['user'] = user['uid']

					for i in range(len(users)):
						if users[i]['uid']==user['uid']:
							for k, v in user.items():
								users[i][k] = v
							user = None
							break
					if user:
						users.append(user)

				else:
					record['user'] = 0

				#进行分词处理
				words_cut = cut_sentence(record['text'])
				record['words'] = words_cut

				texts.append(words_cut)
				records.append(record)

		# 写users
		dump_users(os.path.join(os.path.dirname(__file__), 'result/users'), users)
		# 写入records
		records_hour_file = dump_records(records)
		# 写入texts
		texts_hour_file = dump_texts(texts)

		return [records_hour_file, texts_hour_file]

	except Exception as e:
		print('处理json文件出错: %s' % e)
		return None


if __name__=='__main__':
	DIR = os.path.dirname(__file__)
	filepath = os.path.join(DIR, '../data/data/weibos_hour_1468048975')

	cut_json_file(filepath)

