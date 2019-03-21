# -*- coding: utf-8 -*-
import scrapy
import re
from graduation_project.items import OriginDataDetailItem

BASE_DOMAIN = "http://www.jiangmen.gov.cn/szdwzt/jmtjj/tjsj/tjyb/tjyxjs/"


class EconomicDataSpiderSpider(scrapy.Spider):
    name = 'economic_data_spider'
    allowed_domains = ['jiangmen.gov.cn']
    start_urls = ['http://www.jiangmen.gov.cn/szdwzt/jmtjj/tjsj/tjyb/']

    def parse(self, response):
        if response.status == "404":
            return
        detail_url = response.xpath("//ul[@class='news-group-list']//div[@class='news-group-title']")
        script_text = response.xpath("//div[@class='pages']/div/script/text()").get().strip()
        page_num = re.findall(r"\d", script_text)[0]
        # print('=' * 50)
        # print(response.url)
        for content in detail_url:
            href = content.xpath("./a/@href").get()[2:]
            yield scrapy.Request(url=BASE_DOMAIN + href, callback=self.parse_detail_page)

        for i in range(1, int(page_num)):
            next_page_url = BASE_DOMAIN + 'default_' + str(i) + '.html'
            yield scrapy.Request(next_page_url, callback=self.parse)

    @staticmethod
    def parse_detail_page(response):
        title = response.xpath("//div[@class='news-title']/text()").get()
        pub_message = response.xpath("//div[@class='news-title-date']/text()").get().strip()
        pub_time = ''.join(re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", pub_message))
        pub_source = re.sub(r".+[\s：]", "", pub_message)
        all_content = ''.join(response.xpath("//div[contains(@class, 'TRS_UEDITOR')]//text()").getall())
        all_content = re.sub(r"[\s]", '', all_content)
        current_url = response.url
        origin_data = OriginDataDetailItem(title=title, pub_time=pub_time, pub_source=pub_source,
                                           all_content=all_content, current_url=current_url)
        yield origin_data
