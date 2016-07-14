#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'请求weibo api的requests封装'

__author__='litterzhang'

import requests

class JsonRequest(object):
	"""docstring for JsonRequest"""
	def __init__(self):
		super(JsonRequest, self).__init__()

	#post方法
	def post(url, data={}):
		r = requests.get(url, data=data)
		return JsonRequest.result(r)

	#get方法
	def get(url, data={}):
		r = requests.get(url, params=data)
		return JsonRequest.result(r)

	#处理返回结果
	def result(res):
		result = {}
		res.encoding = 'utf-8'
		try:
			res_obj = res.json()
			if res_obj.get('error', None) and res_obj.get('error_code', None):
				result['success'] = False
				result['error'] = ('ErrorCode: %d, ErrorMsg: %s' % 
					(res_obj['error_code'], res_obj['error']))
				result['request'] = res_obj.get('request', None)
			else:
				result['success'] = True
				result['data'] = res_obj
		except Exception as e:
			result['success'] = False
			result['error'] = ('ErrorCode: %d, ErrorMsg: %s' % (0, e))
			result['data'] = res.text
		return result


