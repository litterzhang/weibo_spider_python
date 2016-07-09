#!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'通过微博客户端获取微博'

__author__='litterzhang'

import requests
import json

from requests.auth import AuthBase

from client_settings import *

class WeiboBaseClient(AuthBase):
	def __init__(self):
		pass

	def __call__(self, r):

		return r

class WeiboRequest(object):
	def __init__(self):
		super(WeiboRequest, self).__init__()

		self._data_base = BASE_AUTH
		self._session = requests.session()
		self._auth = WeiboBaseClient()


	def get(self, url, data={}):
		data = dict(self._data_base, **data)
		r = self._session.get(url, params=data, auth=self._auth)
		return r

	def get_cardlist(self, containerid, page=1, skin='default', count=50):
		data = {
			'containerid': containerid,
			'page': page,
			'skin': skin,
			'count': count
		}
		r = self.get(URL_CARDLIST, data=data)

		result = {'success': False, 'data': []}

		try:
			r.encoding = 'utf-8'
			res_origin = r.json()
			# res_origin = json.load(open('r', 'r', encoding='utf-8'))

			data = list()
			for card in res_origin.get('cards'):
				blog_item = card.get('mblog', None)
				if not blog_item:
					continue

				data_item = {}
				data_item['create_time'] = blog_item.get('created_at', None)
				data_item['text'] = blog_item.get('text')
				data_item['id'] = blog_item.get('id')
				
				blog_user = blog_item.get('user', None)
				if blog_user:
					data_user = dict()
					data_user['uid'] = blog_user.get('id')
					data_user['name'] = blog_user.get('name')
					data_user['location'] = blog_user.get('location')
					data_user['province'] = blog_user.get('province')
					data_user['city'] = blog_user.get('city')
					data_user['statuses_count'] = blog_user.get('statuses_count')
					data_user['followers_count'] = blog_user.get('followers_count')
					data_user['friends_count'] = blog_user.get('friends_count')

					data_item['user'] = data_user
				data.append(data_item)
			result['success'] = True
			result['data'] = data
 
		except Exception as e:
			result['success'] = False
			result['data'] = e
		return result

	def post(self, url, data={}):
		pass