# -*- coding: utf-8 -*-
import scrapy
from SinaNewsSpider.items import SinanewsspiderItem


class SinanewsSpider(scrapy.Spider):
    name = "sinanews"
    allowed_domains = ["finance.sina.com.cn",'search.sina.com.cn']
    start_urls = ['http://search.sina.com.cn/?q=%B1%A3%CF%D5&range=all&c=news&sort=time']

    def parse(self, response):


        # follow links to author pages
        # for href in response.css('.author + a::attr(href)').extract():
        #     yield scrapy.Request(response.urljoin(href),
        #                          callback=self.parse_author)

        for quote in response.css('div.box-result.clearfix'):
            item = SinanewsspiderItem()
            title = quote.css('a::text').extract_first()
            source = quote.css('span::text').extract_first()
            brief = quote.css('p.content::text').extract()
            detail_url = quote.css('a::attr(href)').extract_first()

            item['title'] = title
            item['source'] = source
            item['brief'] = brief
            item['detail_url'] = detail_url
            request= scrapy.Request(response.urljoin(detail_url),
                                     callback=self.parseNews)
            request.meta['item'] = item
            yield  request



        next_page = response.css('div.pagebox a::attr(href)').extract()[-1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parseNews(self,response):
        item = response.meta['item']
        content_list=response.css('div.article p::text').extract()
        content = "".join(content_list)  # 将list转化为string
        # 把内容中的换行符，空格等去掉
        item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '')
        yield item
