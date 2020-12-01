# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    datetime = scrapy.Field()
    # pass

class AbstractItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    abstract = scrapy.Field()
    url = scrapy.Field()
    # tags = scrapy.Field()
    # datetime = scrapy.Field()
    # pass
