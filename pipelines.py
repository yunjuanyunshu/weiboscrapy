# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors
import socket
import select
import sys
import os
import errno

class MySQLStorePipeline(object):

	def __init__(self):
		self.dbpool=adbapi.ConnectionPool('MySQLdb',
			db='test',
			user='root',                                    # this is the username of your mysql
			passwd='y',                                     # this is the passward of your mysql
			cursorclass=MySQLdb.cursors.DictCursor,
			charset='utf8',
			use_unicode=False
		)

	def process_item(self, item, spider):

		query=self.dbpool.runInteraction(self._conditional_insert,item)

		query.addErrback(self.handle_error)
		return item

	def _conditional_insert(self, tx, item):            # creating a table "book" in your test database is needed at first.
		tx.execute("insert into book(content,zhuanfa,pinglun)values(%s,%s,%s)",(item['content'],item['zhuanfa'],item['pinglun']))
