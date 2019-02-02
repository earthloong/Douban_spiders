# -*- coding: utf-8 -*-
import requests
import time
import random
import os
import re
import csv
from multiprocessing.dummy import Pool
from fake_useragent import UserAgent, FakeUserAgentError
from save_data import database

class DB(object):
	def __init__(self):
		try:
			self.ua = UserAgent(use_cache_server=False).random
		except FakeUserAgentError:
			pass
		# self.date = '2000-01-01'
		self.cookie = 'gr_user_id=d5a7e759-8de6-4891-86e0-f72d7485cdfe; __yadk_uid=wia68uVxyxy0tlBxTaTFGjuzXmCX9xeU; _ga=GA1.2.1657514447.1497601281; ue="153821064@qq.com"; _vwo_uuid_v2=8554B4120F8A9E0F9D436E4E28660C7C|2b65ea09ee7861daea34a2bda28b500a; bid=eF71gENcjlQ; ll="118159"; douban-fav-remind=1; viewed="26740503_30187219_30187217_22714154"; __utmv=30149280.18556; __utmc=30149280; __utmc=223695111; ps=y; __utma=30149280.1657514447.1497601281.1542074361.1542112373.66; __utmz=30149280.1542112373.66.42.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1542112373; dbcl2="185568216:IvpIxChr+gY"; ck=nRP-; __utma=223695111.1728141219.1497601282.1542074361.1542112381.48; __utmb=223695111.0.10.1542112381; __utmz=223695111.1542112381.48.26.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1542112381%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=c7bf3f386bbbaa40.1497601282.56.1542112381.1542074398.; _pk_ses.100001.4cf6=*; push_noty_num=0; push_doumail_num=0'
		self.db = database()
		
	def replace(self, x):
		# 去除img标签,7位长空格
		removeImg = re.compile('<img.*?>| {7}|')
		# 删除超链接标签
		removeAddr = re.compile('<a.*?>|</a>')
		# 把换行的标签换为\n
		replaceLine = re.compile('<tr>|<div>|</div>|</p>')
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
		x = re.sub(removeImg, "", x)
		x = re.sub(removeAddr, "", x)
		x = re.sub(replaceLine, "\n", x)
		x = re.sub(replaceTD, "\t", x)
		x = re.sub(replacePara, "", x)
		x = re.sub(replaceBR, "\n", x)
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
		x = re.sub(u'  /  ', '/', x)
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
	
	def p_time(self, stmp):  # 将时间戳转化为时间
		stmp = float(str(stmp)[:10])
		timeArray = time.localtime(stmp)
		otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		return otherStyleTime
	
	def GetProxies(self):
		# 代理服务器
		proxyHost = "http-dyn.abuyun.com"
		proxyPort = "9020"
		# 代理隧道验证信息
		proxyUser = "HK847SP62Z59N54D"
		proxyPass = "C0604DD40C0DD358"
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
	
	def save_sql(self, table_name,items):  # 保存到sql
		all = len(items)
		print all
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
		for item in items:
			try:
				self.db.add(table_name, item)
			except:
				continue
				
	def get_duanping_all(self, project_url, product_number, plat_number):  # 获取短评
		p0 = re.compile('subject/(\d+)')
		subject_id = re.findall(p0, project_url)[0]
		results = []
		url = "https://movie.douban.com/subject/%s/comments" % subject_id
		for kind in ['h', 'm', 'l']:
			page = 1
			while page <= 25:
				print kind, page
				querystring = {"start": str(20 * (page - 1)), "limit": "20", "sort": "new_score", "status": "P",
				               "percent_type": kind, 'comments_only': '1'}
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
					'pragma': "no-cache",
					'accept-encoding': "gzip, deflate, br",
					'accept-language': "zh-CN,zh;q=0.9",
					'user-agent': user_agent,
					'accept': "*/*",
					'referer': "https://movie.douban.com/subject/6390825/comments?start=20&limit=20&sort=new_score&status=P&percent_type=",
					'x-requested-with': "XMLHttpRequest",
					'connection': "keep-alive",
					'cookie':self.cookie
				}
				retry = 3
				t1 = []
				while 1:
					try:
						text = requests.get(url, headers=headers, params=querystring,
						                    timeout=10).text
						p1 = re.compile(
							u'<span class=\\\\"votes\\\\">(.*?)</span>.*?<a href=\\\\"https://www\.douban\.com/people.*?>(.*?)</a>(.*?)<span class=\\\\"comment-time \\\\".*?title=\\\\"(.*?)\\\\">.*?<p class=\\\\"\\\\">(.*?)</p>',
							re.S)
						items = re.findall(p1, text)
						last_modify_date = self.p_time(time.time())
						for item in items:
							nick_name = item[1].decode('unicode_escape', 'ignore')
							like_cnt = item[0]
							cmt_reply_cnt = '0'
							long_comment = '0'
							source_url = project_url
							if 'allstar' in item[2]:
								try:
									p2 = re.compile('allstar(\d+)')
									ss = re.findall(p2, item[2])[0]
									score = int(ss) / 10.0
								except:
									score = 0
							else:
								score = 0
							cmt_date = item[3].split()[0]
							# if cmt_date < self.date:
							# 	continue
							cmt_time = item[3]
							comments = self.replace(item[4].decode('unicode_escape', 'ignore'))
							tmp = [product_number, plat_number, nick_name, cmt_date, cmt_time, comments, like_cnt,
							       cmt_reply_cnt, long_comment, last_modify_date, source_url]
							tt = '|'.join(tmp)
							print tt
							if tt not in results:
								results.append(tt)
								t1.append([x.encode('gbk', 'ignore') for x in tmp])
						print len(t1)
						if len(t1) > 0:

							# with open('data_comments.csv', 'a') as f:
							# 	writer = csv.writer(f, lineterminator='\n')
							# 	writer.writerows(t1)

							print u'%s 开始录入数据库' % product_number
							self.save_sql('T_COMMENTS_PUB_MOVIE', t1)  # 手动修改需要录入的库的名称
							print u'%s 录入数据库完毕' % product_number
							break
						else:
							break
					except Exception as e:
						retry -= 1
						if retry == 0:
							print e
							return None
						else:
							continue
				page += 1
	
	def get_duanping_xiangkan(self, project_url, product_number, plat_number):  # 获取短评
		p0 = re.compile('subject/(\d+)')
		subject_id = re.findall(p0, project_url)[0]
		url = "https://movie.douban.com/subject/%s/comments" % subject_id
		for kind in ['']:
			page = 1
			while page <= 25:
				print 'kind:',kind, 'page:',page
				querystring = {"start": str(20 * (page - 1)), "limit": "20", "sort": "new_score", "status": "F",
				               "percent_type": '', 'comments_only': '1'}
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
					'pragma': "no-cache",
					'accept-encoding': "gzip, deflate, br",
					'accept-language': "zh-CN,zh;q=0.9",
					'user-agent': user_agent,
					'accept': "*/*",
					'referer': "https://movie.douban.com/subject/6390825/comments?start=20&limit=20&sort=new_score&status=P&percent_type=",
					'x-requested-with': "XMLHttpRequest",
					'connection': "keep-alive",
					'cookie':self.cookie
				}
				retry = 3
				t1 = []
				results = []
				while page <= 10:
					try:
						text = requests.get(url, headers=headers, params=querystring,
						                    timeout=10).text
						p1 = re.compile(
							u'<span class=\\\\"votes\\\\">(.*?)</span>.*?<a href=\\\\"https://www\.douban\.com/people.*?>(.*?)</a>(.*?)<span class=\\\\"comment-time \\\\".*?title=\\\\"(.*?)\\\\">.*?<p class=\\\\"\\\\">(.*?)</p>',
							re.S)
						items = re.findall(p1, text)
						last_modify_date = self.p_time(time.time())
						for item in items:
							nick_name = item[1].decode('unicode_escape', 'ignore')
							like_cnt = item[0]
							cmt_reply_cnt = '0'
							long_comment = '0'
							source_url = project_url
							if 'allstar' in item[2]:
								try:
									p2 = re.compile('allstar(\d+)')
									ss = re.findall(p2, item[2])[0]
									score = int(ss) / 10.0
								except:
									score = 0
							else:
								score = 0
							cmt_date = item[3].split()[0]
							# if cmt_date < self.date:
							# 	continue
							cmt_time = item[3]
							comments = self.replace(item[4].decode('unicode_escape', 'ignore'))
							tmp = [product_number, plat_number, nick_name, cmt_date, cmt_time, comments, like_cnt,
							       cmt_reply_cnt, long_comment, last_modify_date, source_url]
							tt = '|'.join(tmp)
							print tt
							if tt not in results:
								results.append(tt)
								t1.append([x.encode('gbk', 'ignore') for x in tmp])
						print len(t1)
						if len(t1) > 0:

							# with open('data_comments.csv', 'a') as f:
							# 	writer = csv.writer(f, lineterminator='\n')
							# 	writer.writerows(t1)

							print u'%s 开始录入数据库' % product_number
							self.save_sql('T_COMMENTS_PUB_MOVIE', t1)  # 手动修改需要录入的库的名称
							print u'%s 录入数据库完毕' % product_number
							break
						else:
							break
					except Exception as e:
						retry -= 1
						if retry == 0:
							print e
							return None
						else:
							continue
				page += 1


if __name__ == "__main__":
	db = DB()
	s = []
	with open('new_data.csv') as f:
		tmp = csv.reader(f)
		for i in tmp:
			if 'http' in i[2]:
				s.append([i[2], i[0], 'P09'])
	for j in s:
		print j[1],j[0]
		db.get_duanping_all(j[0], j[1], j[2])
		db.get_duanping_xiangkan(j[0], j[1], j[2])
	db.db.db.close()
