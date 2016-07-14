#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'抓取欧洲杯相关微博'

__author__='litterzhang'

import time
import json

from weiboclient import WeiboRequest
from spider_settings import ContainerId

def weibo_get_by_client(containerid):
	res = WeiboRequest().get_cardlist(containerid)
	if res['success']:
		with open('data/weibo_%s' % str(int(time.time())), 'w', encoding='utf-8') as fr:
			json.dump(res['data'], fr, ensure_ascii=False)
	return res['success']

def worker():
	index = 0
	while True:
		res = weibo_get_by_client(ContainerId[index])
		index = (index + 1)%len(ContainerId)

		if res:
			time.sleep(100)
		else:
			time.sleep(200)

if __name__=='__main__':
	worker()
