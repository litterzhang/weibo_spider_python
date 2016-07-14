#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'下载验证码'

__author__='litterzhang'

import time
import requests

from bs4 import BeautifulSoup

#下载验证码
def fetch_captcha(res):
	if res.status_code==200:
		try:
			res.encoding = 'utf-8'
			soup = BeautifulSoup(res.text, 'html.parser')

			# print(res.text)
			captcha_id_items = soup.select('input[name=capId]')
			# print(len(captcha_id_items))
			if len(captcha_id_items):
				captcha_id = captcha_id_items[0]['value']
				# print(captcha_id)

				r_img = requests.get('http://weibo.cn/interface/f/ttt/captcha/show.php', \
					params={'cpt': captcha_id})
				if r_img.status_code==200:
					with open('img/img_%s.png' % (str(int(time.time()))), 'wb') as fw:
						fw.write(r_img.content)
		except Exception as e:
			print(e)

#请求获取验证码
def request_for_captcha():
	try:
		r = requests.get('http://login.weibo.cn/login/')	
		if r.status_code==200:
			fetch_captcha(r)
		else:
			print(r.status_code)
	except Exception as e:
		print(e)

if __name__=='__main__':
	count = 0
	while True:
		request_for_captcha()
		count += 1
		# if count>1000:
		# 	break