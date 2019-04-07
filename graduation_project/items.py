# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GraduationProjectItem(scrapy.Item):
    db_symbol = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    pub_time = scrapy.Field()
    pub_source = scrapy.Field()
    all_content = scrapy.Field()
    indicator_name = scrapy.Field()
    indicator_unit = scrapy.Field()
    indicator_amount = scrapy.Field()
    indicator_percentage_increase = scrapy.Field()
    current_url = scrapy.Field()