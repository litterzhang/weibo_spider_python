#!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'通过微博sdk获取微博'

__author__='litterzhang'

import requests
import json

from json_requests import JsonRequest
from setting import *

class WeiboClient(object):
	"""微博sdk客户端"""
	def __init__(self,):
		super(WeiboClient, self).__init__()

		self._init_success = True

		#设置access_token
		access_token = None
		try:
			with open('access_token', 'r', encoding='utf-8') as fr:
				access_token = json.load(fr)
				print(access_token)

		except Exception as e:
			access_token = self.get_access_token(**OAuth2Data)
		finally:
			self._access_token = access_token.get('access_token', None)
			self._uid = access_token.get('uid', None)

		#检测access_token是否可用，及api频次
		if not self._access_token or not self._uid:
			self._init_success = False
			return
		else:
			r = JsonRequest.get('https://api.weibo.com/2/account/rate_limit_status.json',
				data={'access_token': self._access_token})
			
			print(json.dumps(r))


	def get_access_token(self, AppKey, AppSercet, Code, RedirectUri):
		payload = {'client_id': AppKey, 'client_secret': AppSercet, 
					'grant_type': 'authorization_code', 'code': Code, 
					'redirect_uri': RedirectUri}
		r = requests.post('https://api.weibo.com/oauth2/access_token', data=payload)

		r.encoding = 'utf-8'
		access_token = r.json()

		with open('access_token', 'w', encoding='utf-8') as fw:
			json.dump(access_token, fw, ensure_ascii=False)
		return access_token

weibo = WeiboClient()
