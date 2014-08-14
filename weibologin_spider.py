# -*- coding: utf-8 -*-
import scrapy
import time
import re,json
import os
import urllib,urllib2,urllib3,cookielib
import rsa,binascii
from weibologin.items import WeibologinItem
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy import log

class WeibologinSpider(scrapy.Spider):
	name = "weibologin"
	allowed_domains = ["weibo.com","localhost"]
	start_urls = [
		"http://www.weibo.com"
	]

	# 获取一个保存cookie的对象
	cj = cookielib.LWPCookieJar()
	# 将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
	cookie_support = urllib2.HTTPCookieProcessor(cj)
	# 创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
	# 将包含了cookie、http处理器、http的handler的资源和urllib2对象板顶在一起
	urllib2.install_opener(opener)

	def get_password_rsa(self,USER_PSWD,PUBKEY,servertime,nonce):
		self.log("00000")
		rsaPubkey=int(PUBKEY,16)
		key_1=int('10001',16)
		key=rsa.PublicKey(rsaPubkey,key_1)
		message=str(servertime)+"\t"+str(nonce)+"\n"+str(USER_PSWD)
		passwd=rsa.encrypt(message,key)
		passwd=binascii.b2a_hex(passwd)# to h
		return passwd

	def parse(self, response):
		USER_PSWD='haohao'
		su='eGQ0NzEwNSU0MDEyNi5jb20='  # 微博账户名（固定），firebug抓包可见
		url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack\
&su="+su+"&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)"
		r=urllib3.PoolManager().request('GET',url)
		p=re.compile('\((.*)\)')
		json_data=p.search(r.data).group(1)
		data=json.loads(json_data)
		PUBKEY=data['pubkey']
		servertime=str(data['servertime'])
		nonce=data['nonce']
		sp=self.get_password_rsa(USER_PSWD,PUBKEY,servertime,nonce)
		formdata={"encoding":'UTF-8',
			"entry":'weibo',
			"from":'', 
			"gateway":'1',
			"nonce":nonce,
			"pagerefer":'',# 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
			"prelt":'0',
			"pwencode":'rsa2',
			"returntype":"META",
			"rsakv":'1330428213',
			"savestate":'7',
			"servertime":servertime,# str(int(time.time())),
			"service":'miniblog',
			"sp":sp,
			"sr":'1173*733',
			"su":'eGQ0NzEwNSU0MDEyNi5jb20=',
			"url":'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
			"useticket":'1',
			"vsnf":'1'}
		data = urllib.urlencode(formdata)# 必须有，把dictionary转为string，data须为string
		http_headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0'}
		self.log("66666")
		
		req = urllib2.Request('http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)',data,http_headers);
		result = urllib2.urlopen(req)
		text = result.read()
		p = re.compile('location\.replace\(\'(.*?)\'\)')
		try:
			login_url = p.search(text).group(1)
			print login_url
			urllib2.urlopen(login_url)
			print "login success"
		except:
			print 'Login error!'
#		req = urllib2.Request(url='http://weibo.com/Laruence')
		result = urllib2.urlopen('http://weibo.com/Laruence')
		fff=open("/var/www/lar.html",'w')
		fff.write(result.read().replace(r'\"',"'").replace(r'\n','').replace(r'\r','').replace(r'\t','').replace(r'<script>FM.view({"ns":"pl.content.homeFeed.index","domid":"Pl_Core_OwnerFeed__3","css":["style/css/module/frameset/comb_PRF_feed.css?version=','').replace(r'"],"js":"page/js/pl/content/homeFeed/index.js?version=','').replace(r'","html":','').replace('"','').replace(r'\/','/'))
		return Request("http://localhost/lar.html",callback=self.parse_lar,dont_filter=True)

	def parse_lar(self,response):
		nodes = response.xpath('//div[@class="WB_detail"]')
		for node in nodes:
			item = WeibologinItem()
			item['content1'] = ' '.join(node.xpath('.//div[@node-type="feed_list_content"]/text() | .//div[@node-type="feed_list_content"]/a/text()').extract())
			item['content2'] = ' '.join(node.xpath('.//div[@class="WB_info"]/a/text() | .//div[@node-type="feed_list_reason"]/em/text() | .//div[@node-type="feed_list_reason"]/em/a/text()').extract())
 			item['zhuanfa1'] = ' '.join(node.xpath('.//div[@class="WB_handle"]/a[contains(@action-type,"fl_forward")]/text()').re('\d+'))
			item['zhuanfa2'] = ' '.join(node.xpath('.//div[@mid]/a[2]/text()').re('\d+'))
			item['pinglun1'] = ' '.join(node.xpath('.//div[@class="WB_handle"][1]/a[4]/text()').re('\d+'))
			item['pinglun2'] = ' '.join(node.xpath('.//div[@mid]/a[3]/text()').re('\d+'))
			yield item
