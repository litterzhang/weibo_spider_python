#!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'获取代理ip地址'

__author__='litterzhang'

import requests
import time

from bs4 import BeautifulSoup

#从xici代理获取代理ips
def get_proxy_ips():
	r = requests.get('http://www.xicidaili.com/nn/', 
		headers={'User-Agent': 'Mozilla/2.02E (Win95; U)'})
	#r.encoding = 'utf-8'
	
	soup = BeautifulSoup(r.text, 'html.parser')

	res_ips = list()

	ips_list = soup.select('table#ip_list > tr')[1:]
	for ip_item in ips_list:
		ip_attrs = ip_item.select('td')

		res_ip = dict()
		res_ip['addr'] = ip_attrs[1].text.strip()
		res_ip['port'] = ip_attrs[2].text.strip()
		res_ip['loc'] = ip_attrs[3].text.strip()
		res_ip['type'] = ip_attrs[5].text.strip().lower()

		if test_proxy_ip(res_ip):
			res_ips.append(res_ip)
	return res_ips

#测试代理的可用性
def test_proxy_ip(ip):
	proxies = dict()

	#若代理信息不全
	if not ip.get('addr') or not ip.get('port') or \
		not ip.get('type') or ip['type'] not in ['http', 'https']:
		return False

	proxies[ip['type']] = ('%s://%s:%s' % (ip['type'], ip['addr'], ip['port']))

	#请求weibo页面测试
	try:
		r = requests.get('http://login.weibo.cn/login/', proxies=proxies, timeout=0.5)	
		
		if res.status_code==200:
			return True
	except Exception as e:
		return False		


ips = get_proxy_ips()
print(ips)