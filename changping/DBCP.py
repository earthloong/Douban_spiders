# -*- coding: utf-8 -*-
import requests
import time
import random
import os
import re
import csv
import json
import sys
import datetime
from multiprocessing.dummy import Pool
from fake_useragent import UserAgent, FakeUserAgentError
from save_data import database

class DB(object):
	def __init__(self):
		self.data = []
		try:
			self.ua = UserAgent(use_cache_server=False).random
		except FakeUserAgentError:
			pass
		# self.date = '2000-01-01'
		self.db = database()
	
	def replace(self, x):
		# 去除img标签,7位长空格
		removeImg = re.compile('<img.*?>| {7}|')
		# 删除超链接标签
		removeAddr = re.compile('<a.*?>|</a>')
		# 把换行的标签换为\n
		replaceLine = re.compile('<tr>|<div>|</div>')
		# 将表格制表<td>替换为\t
		replaceTD = re.compile('<td>')
		# 把段落开头换为\n加空两格
		replacePara = re.compile('<p.*?>')
		# 将换行符或双换行符替换为\n
		replaceBR = re.compile('<br><br>|<br>')
		# 将其余标签剔除
		removeExtraTag = re.compile('<.*?>', re.S)
		# 将&#x27;替换成'
		replacex27 = re.compile('&#x27;')
		# 将&gt;替换成>
		replacegt = re.compile('&gt;|&gt')
		# 将&lt;替换成<
		replacelt = re.compile('&lt;|&lt')
		# 将&nbsp换成''
		replacenbsp = re.compile('&nbsp;')
		# 将&#x2715;&#x2715;,换成''
		replace2715 = re.compile('&#x2715;&#x2715;,')
		replace1 = re.compile(',')
		x = re.sub(removeExtraTag, '', x)
		x = re.sub(replacex27, '\'', x)
		x = re.sub(replacegt, '>', x)
		x = re.sub(replacelt, '<', x)
		x = re.sub(replacenbsp, '', x)
		x = re.sub(replace2715, '', x)
		x = re.sub(replace1, '', x)
		x = re.sub(re.compile('&#183;'), u'.', x)
		x = re.sub(u'&#39;', '\'', x)
		x = re.sub(re.compile('\\\\n'), ' ', x)
		x = re.sub(re.compile('\s'), u'  ', x)
		x = re.sub(re.compile('[\r\n]'), u'  ', x)
		return x.strip()
	
	def get_headers(self):
		user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
		               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
		               'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
		               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
		               'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
		               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
		               'Opera/9.52 (Windows NT 5.0; U; en)',
		               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.2pre) Gecko/2008071405 GranParadiso/3.0.2pre',
		               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.0 Safari/534.3',
		               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.4 Safari/532.0',
		               'Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.7.39 Version/11.00']
		user_agent = random.choice(user_agents)
		headers = {'Host': 'movie.douban.com',
		           'Connection': 'keep-alive',
		           'User-Agent': user_agent,
		           'Referer': 'https://movie.douban.com/subject/26904663/',
		           'Accept-Encoding': 'gzip, deflate, br',
		           'Accept-Language': 'zh-CN,zh;q=0.8'
		           }
		return headers
	
	def GetProxies(self):
		# 代理服务器
		proxyHost = "http-dyn.abuyun.com"
		proxyPort = "9020"
		# 代理隧道验证信息
		proxyUser = "HI18001I69T86X6D"
		proxyPass = "D74721661025B57D"
		proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
			"host": proxyHost,
			"port": proxyPort,
			"user": proxyUser,
			"pass": proxyPass,
		}
		proxies = {
			"http": proxyMeta,
			"https": proxyMeta,
		}
		return proxies
	
	def get_detail2(self, item):  # 获取豆瓣长评
		results = []
		results.extend(item)
		url = item[-1]
		print url
		retry = 20
		while 1:
			try:
				user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
							   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
							   'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
							   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
							   'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
							   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
							   'Opera/9.52 (Windows NT 5.0; U; en)',
							   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.2pre) Gecko/2008071405 GranParadiso/3.0.2pre',
							   'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.0 Safari/534.3',
							   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.4 Safari/532.0',
							   'Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.7.39 Version/11.00']
				user_agent = random.choice(user_agents)
				headers = {
					'host': "movie.douban.com",
					'connection': "keep-alive",
					'cache-control': "no-cache",
					'upgrade-insecure-requests': "1",
					'user-agent': user_agent,
					'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
					'referer': "https://movie.douban.com/subject/25975243/",
					'accept-encoding': "gzip, deflate, br",
					'accept-language': "zh-CN,zh;q=0.9"
				}
				text = requests.get(url, headers=headers, proxies=self.GetProxies(), timeout=10).text
				p0 = re.compile(u'<div class="main-bd">(.*?)<div class="main-author">', re.S)
				content = self.replace(re.findall(p0, text)[0])
				# print items
				comments = content.replace(u'这篇影评可能有剧透', '').strip()
				results[5] = comments
				# print results
				tt = [x.encode('gbk', 'ignore') for x in results]
				return tt
			except Exception as e:
				retry -= 1
				if retry == 0:
					print e
					tt = [x.encode('gbk', 'ignore') for x in results]
					return tt
				else:
					continue

	def p_time(self, stmp):  # 将时间戳转化为时间
		stmp = float(str(stmp)[:10])
		timeArray = time.localtime(stmp)
		otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		return otherStyleTime
	
	def get_all_id(self, ss):  # 获取所有长评id
		subject_id, product_number, plat_number, page = ss
		print 'page:',page
		url = "https://movie.douban.com/subject/%s/reviews" % subject_id
		querystring = {"start": str((page - 1) * 20)}
		retry = 5
		while 1:
			results = []
			try:
				user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
							   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
							   'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
							   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
							   'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
							   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
							   'Opera/9.52 (Windows NT 5.0; U; en)',
							   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.2pre) Gecko/2008071405 GranParadiso/3.0.2pre',
							   'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.0 Safari/534.3',
							   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.4 Safari/532.0',
							   'Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.7.39 Version/11.00']
				user_agent = random.choice(user_agents)
				headers = {
					'host': "movie.douban.com",
					'connection': "keep-alive",
					'cache-control': "no-cache",
					'upgrade-insecure-requests': "1",
					'user-agent': user_agent,
					'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
					'referer': "https://movie.douban.com/subject/25975243/",
					'accept-encoding': "gzip, deflate, br",
					'accept-language': "zh-CN,zh;q=0.9"
				}
				text = requests.get(url, headers=headers, params=querystring, proxies=self.GetProxies(),
				                    timeout=10).text
				break
			except Exception as e:
				retry -= 1
				if retry == 0:
					print e
					return None
				else:
					continue
				# print text
		p0 = re.compile(u'class="name">(.*?)</a>.*?class="allstar(\d+).*?class="main-meta">(.*?)</span>.*?<h2><a href="https://movie\.douban\.com/review/(.*?)/">(.*?)</a></h2>.*?title="有用">.*?<span id=.*?>(.*?)</span>.*?<span id=.*?>(.*?)</span>.*?class="reply">(.*?)回应</a>',re.S)
		items = re.findall(p0, text)
		last_modify_date = self.p_time(time.time())
		for item in items:
			nick_name = item[0]
			cmt_date = item[2].split()[0]
			# if cmt_date < self.date:
			# 	continue
			cmt_time = item[2]
			source_url = "https://movie.douban.com/review/%s" % item[3]
			long_comment = '1'
			like_cnt, cmt_reply_cnt = item[5].strip(), item[7].strip()
			if len(like_cnt) == 0:
				like_cnt = '0'
			if len(cmt_reply_cnt) == 0:
				cmt_reply_cnt = '0'
			comments = ''
			tmp = [product_number, plat_number, nick_name, cmt_date, cmt_time, comments, like_cnt,
			       cmt_reply_cnt, long_comment, last_modify_date, source_url]
			print '|'.join(tmp)
			results.append(tmp)
		return results
	
	def get_changping_pagenums(self, subject_id):  # 获取长评的总页数
		url = 'https://movie.douban.com/subject/%s/reviews' % subject_id
		retry = 5
		while 1:
			try:
				user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
							   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
							   'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
							   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
							   'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
							   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
							   'Opera/9.52 (Windows NT 5.0; U; en)',
							   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.2pre) Gecko/2008071405 GranParadiso/3.0.2pre',
							   'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.0 Safari/534.3',
							   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.4 Safari/532.0',
							   'Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.7.39 Version/11.00']
				user_agent = random.choice(user_agents)
				# user_agent = self.ua.chrome,
				# a = list(user_agent)
				# user_agent = a[0]
				headers = {
					'host': "movie.douban.com",
					'connection': "keep-alive",
					'cache-control': "no-cache",
					'upgrade-insecure-requests': "1",
					'user-agent': user_agent,
					'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
					'referer': "https://movie.douban.com/subject/25975243/",
					'accept-encoding': "gzip, deflate, br",
					'accept-language': "zh-CN,zh;q=0.9"
				}
				text = requests.get(url, headers=headers, proxies=self.GetProxies(), timeout=10).text
				
				try:
					p0 = re.compile(u'<a href="\?start=\d+?" >(\d+?)</a>')
					pagenums = re.findall(p0, text)[-1]
					return int(pagenums)
				except:
					if u'<header class="main-hd">' not in text:
						return None
					else:
						pagenums = 1
						return pagenums
			except Exception as e:
				retry -= 1
				if retry == 0:
					print e
					return None
				else:
					continue

	def save_sql(self, table_name,items):  # 保存到sql
		all = len(items)
		print 'all:',all
		results = []
		for i in items:
			try:
				t = [x.decode('gbk', 'ignore') for x in i]
				dict_item = {'product_number': t[0],
				             'plat_number': t[1],
				             'nick_name': t[2],
				             'cmt_date': t[3],
				             'cmt_time': t[4],
				             'comments': t[5],
				             'like_cnt': t[6],
				             'cmt_reply_cnt': t[7],
				             'long_comment': t[8],
				             'last_modify_date': t[9],
				             'src_url': t[10]}
				results.append(dict_item)
			except:
				continue
		for item in results:
			try:
				self.db.add(table_name, item)
			except:
				continue
	
	def get_changping_all(self, project_url, product_number, plat_number):  # 获取某个产品的所有豆瓣长评
		p0 = re.compile('subject/(\d+)')
		subject_id = re.findall(p0, project_url)[0]
		pagenums = self.get_changping_pagenums(subject_id)
		if pagenums is None:
			print u'%s 抓取出错' % product_number
			return None
		else:
			print u'%s 共有 %d 页' % (product_number, pagenums)
			s1 = []
			for page in range(1, pagenums + 1):
				s1.append([subject_id, product_number, plat_number, page])
			pool = Pool(8)
			items = pool.map(self.get_all_id, s1)
			pool.close()
			pool.join()
			mm = []
			for item in items:
				if item is not None:
					mm.extend(item)
			print len(mm)
			pool = Pool(8)
			items = pool.map(self.get_detail2, mm)
			pool.close()
			pool.join()
			'''
			with open('comments.csv', 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerows(items)
			'''
			print u'%s 开始录入数据库' % product_number
			self.save_sql('T_COMMENTS_PUB', items)  # 手动修改需要录入的库的名称
			print u'%s 录入数据库完毕' % product_number


if __name__ == "__main__":
	db = DB()
	s = []
	with open('data.csv') as f:
		tmp = csv.reader(f)
		for i in tmp:
			if 'http' in i[2]:
				s.append([i[2], i[0], 'P09'])
	for j in s:
		print j[1],j[0]
		db.get_changping_all(j[0], j[1], j[2])
	db.db.db.close()
