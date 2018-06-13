#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import scrapy


class GithubSpider(scrapy.Spider):
    """所有 scrapy 爬蟲需要寫一個 Spider 類，這個類要繼承 scrapy.Spider 類。在這個類中定義要請求的網站和鏈接、如何從返回的網頁提取數據等等。"""
    # 爬蟲標識符號，在 scrapy 項目中可能會有多個爬蟲，name 用於標識每個爬蟲，不能相同
    name = 'GithubRepos'

    @property
    def start_urls(self):
        # 課程列表頁面 url 模版
        url_templ = 'https://github.com/shiyanlou?page={}&tab=repositories'
        # 所有要爬取的頁面
        urls = (url_templ.format(i) for i in range(1, 5))
        # 返回一個生成器，生成 Request 對象，生成器是可迭代對象
        # `scrapy`內部的下載器會下載每個`Request`，然後將結果封裝為`response`對象傳入`parse`方法，這個對象和前面scrapy shell
        # 練習中的對象是一樣的，也就是說你可以用`response.css()`或者`response.xpath()`來提取數據了。
        return urls

    def parse(self, response):
        for repo in response.css('li.col-12'):
            yield {
                'name': repo.css('div.d-inline-block a[itemprop="name codeRepository"]::text').extract_first(),
                'update_time': repo.css('div.f6 relative-time::attr(datetime)').extract_first()
            }
