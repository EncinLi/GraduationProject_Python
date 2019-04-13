# -*- coding: utf-8 -*-
import scrapy
import re
from graduation_project.items import GraduationProjectItem

BASE_DOMAIN = "http://www.jiangmen.gov.cn/szdwzt/jmtjj/tjsj/tjyb/"
COMPONENT_DEFAULT = 'default_'
COMPONENT_HTML = '.html'
TARGET_TJYXJS = 'tjyxjs/'
TARGET_ZYJJZB = 'zyjjzb/'
TARGET_GYZJZ = 'gyzjz/'


class EconomicDataSpiderSpider(scrapy.Spider):
    name = 'economic_data_spider'
    allowed_domains = ['jiangmen.gov.cn']
    # start_urls = ['http://www.jiangmen.gov.cn/szdwzt/jmtjj/tjsj/tjyb/tjyxjs/',
    #               'http://www.jiangmen.gov.cn/szdwzt/jmtjj/tjsj/tjyb/zyjjzb/',
    #               'http://www.jiangmen.gov.cn/szdwzt/jmtjj/tjsj/tjyb/gyzjz/']
    start_urls = ['http://www.jiangmen.gov.cn/szdwzt/jmtjj/tjsj/tjyb/zyjjzb/']

    def parse(self, response):
        if response.status == "404":
            return
        detail_url = response.xpath("//ul[@class='news-group-list']//div[@class='news-group-title']")
        script_text = response.xpath("//div[@class='pages']/div/script/text()").get().strip()
        page_num = re.findall(r"\d", script_text)[0]

        for content in detail_url:
            href = content.xpath("./a/@href").get()[2:]
            if href is not None and TARGET_TJYXJS in response.url:
                pass
                # yield scrapy.Request(url=BASE_DOMAIN + TARGET_TJYXJS + href, callback=self.parse_detail_page, dont_filter=True)
            elif href is not None and TARGET_ZYJJZB in response.url:
                yield scrapy.Request(url=BASE_DOMAIN + TARGET_ZYJJZB + href,
                                     callback=self.parse_main_economic_indicator_page)

        for i in range(1, int(page_num)):
            if TARGET_TJYXJS in response.url:
                next_page_url = BASE_DOMAIN + TARGET_TJYXJS + COMPONENT_DEFAULT + str(i) + COMPONENT_HTML
            elif TARGET_ZYJJZB in response.url:
                next_page_url = BASE_DOMAIN + TARGET_ZYJJZB + COMPONENT_DEFAULT + str(i) + COMPONENT_HTML
            elif TARGET_GYZJZ in response.url:
                next_page_url = BASE_DOMAIN + TARGET_GYZJZ + COMPONENT_DEFAULT + str(i) + COMPONENT_HTML

            # next_page_url = BASE_DOMAIN + TARGET_GYZJZ + COMPONENT_DEFAULT + str(i) + COMPONENT_HTML
            yield scrapy.Request(next_page_url, callback=self.parse)

    @staticmethod
    def parse_detail_page(response):
        title = response.xpath("//div[@class='news-title']/text()").get()
        pub_message = response.xpath("//div[@class='news-title-date']/text()").get().strip()
        pub_time = ''.join(re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", pub_message))
        pub_source = re.sub(r".+[\s：]", "", pub_message)
        content_position = response.xpath("//div[contains(@class, 'TRS_UEDITOR')]")
        all_content = ''.join(content_position.xpath(".//text()").extract())
        all_content = re.sub(r"[\s]", '', all_content)
        current_url = response.url

        origin_data = GraduationProjectItem(db_symbol='origin_message', title=title, pub_time=pub_time,
                                              pub_source=pub_source, all_content=all_content, current_url=current_url)
        yield origin_data

    @staticmethod
    def parse_main_economic_indicator_page(response):
        title = response.xpath("//div[@class='news-title']/text()").get()
        month_range = ''
        month = ''
        current_url = response.url
        year = ''.join(re.findall(r"\d{4}", title))

        trs = response.xpath("//tbody/tr")
        for tr in trs:
            td_month = ''.join(tr.xpath("./td[3]/p//text()").extract()).strip()
            indicator_name = ''.join(tr.xpath("./td[1]/p//text()").extract()).strip()
            indicator_unit = ''.join(tr.xpath("./td[2]/p//text()").extract()).strip()
            indicator_amount = ''.join(tr.xpath("./td[3]/p//text()").extract()).strip()
            indicator_percentage_increase = ''.join(tr.xpath("./td[4]/p//text()").extract()).strip()

            if td_month is not None and '月' in td_month:
                month_range = re.sub(r'月', '', td_month)
                month = month_range.split('-')[1]

            if indicator_name == '' or indicator_name == '指标':
                continue
            else:
                if indicator_amount == '---':
                    indicator_amount = re.sub(r'---', '0', indicator_amount)

                # print("=" * 20)
                # print('||' + month_range + '^^^^^^^^' + month + '||')
                # print(indicator_name + '||' + indicator_unit + '||' + indicator_amount +
                #       '||' + indicator_percentage_increase + '||')
                # print("=" * 20)

                main_economic_indicator = GraduationProjectItem(db_symbol='main_economic_indicator', title=title,
                                                                year=year, month_range=month_range, month=month,
                                                                indicator_name=indicator_name,
                                                                indicator_unit=indicator_unit,
                                                                indicator_amount=indicator_amount,
                                                                indicator_percentage_increase=indicator_percentage_increase)
                yield main_economic_indicator

