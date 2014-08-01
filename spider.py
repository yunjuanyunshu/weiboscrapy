# -*- coding: utf-8 -*-
import scrapy

from weibonumerous.items import WeibonumerousItem    # Weibonumerous should all be replaced with ProjectnameItem 
                                                     # weibonumerous should all be replaced with projectnameItem
class WeibonumerousSpider(scrapy.Spider):
	name = "weibonumerous"
	allowed_domains = ["localhost"]
	start_urls = [
		"http://localhost/Laruence的微博.html"
	]

	def parse(self, response):
		nodes = response.xpath('//div[@class="WB_detail"]')
		for node in nodes:
			item = WeibonumerousItem()
			item['content'] = ' '.join(node.xpath('.//div[@class="WB_text"]/p/em/text()').extract())
			item['zhuanfa'] = ' '.join(node.xpath('.//div[@class="WB_handle"]/a[2]/text()').re('\d+'))
			item['pinglun'] = ' '.join(node.xpath('.//div[@class="WB_handle"]/a[4]/text()').re('\d+'))
			yield item
