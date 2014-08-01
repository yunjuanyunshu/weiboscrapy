# -*- coding: utf-8 -*-

# Scrapy settings for weibonumerous project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'weibonumerous'              # weibonumerous should all be replaced with your projectname

SPIDER_MODULES = ['weibonumerous.spiders']
NEWSPIDER_MODULE = 'weibonumerous.spiders'

ITEM_PIPELINES={
	'weibonumerous.pipelines.MySQLStorePipeline'
}
