# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibonumerousItem(scrapy.Item):# Weibonumerous in this line should be replaced with your projectname
	content = scrapy.Field()
	zhuanfa = scrapy.Field()
	pinglun = scrapy.Field()
