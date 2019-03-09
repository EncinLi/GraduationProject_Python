# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EconomicDataSpiderSpider(CrawlSpider):
    name = 'economic_data_spider'
    allowed_domains = ['www.jiangmen.gov.cn/szdwzt/jmtjj/']
    start_urls = ['http://www.jiangmen.gov.cn/szdwzt/jmtjj//']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=False)
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
