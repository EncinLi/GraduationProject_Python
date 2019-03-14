# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class EconomicDataSpiderSpider(CrawlSpider):
    name = 'economic_data_spider'
    allowed_domains = ['jiangmen.gov.cn']
    start_urls = ['http://www.jiangmen.gov.cn/szdwzt/jmtjj/tjsj/tjyb/tjyxjs/']

    rules = (
        Rule(LinkExtractor(allow=r'.+default_\d\.html'), follow=True),
        Rule(LinkExtractor(allow=r'.+t[\d]{8}_[\d]{7}\.html'), callback='parse_detail_page', follow=False),
    )

    def parse_detail_page(self, response):
        title = response.xpath("//div[@class='news-title']/text()").get()
        pub_title = response.xpath("//div[@class='news-title-date']/text()").get().strip()
        pub_time = ''.join(re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", pub_title))
        pub_resource = re.sub(r".+[\s：]", "", pub_title)
        all_content = ''.join(response.xpath("//div[contains(@class, 'view TRS_UEDITOR trs_paper_default')]//text()").getall()).strip()
        all_content = re.sub(r"[\s]", '', all_content)
        print("=" * 40)
        print(all_content)
        print("=" * 40)
