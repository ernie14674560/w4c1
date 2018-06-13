#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import scrapy


class GithubSpider(scrapy.Spider):
    name = 'GithubRepos'

    @property
    def start_urls(self):
        url_templ = 'https://github.com/shiyanlou?page={}&tab=repositories'
        urls = (url_templ.format(i) for i in range(1, 5))
        return urls

    def parse(self, response):
        for repo in response.css('li.col-12'):
            yield {
                #'name': repo.css('div.d-inline-block a[itemprop="name codeRepository"]::text').extract_first(),
                #'update_time': repo.css('div.f6 relative-time::attr(datetime)').extract_first()
                'name': repo.css('a::text').extract_first().strip(),
                'update_time': repo.css('relative-time::attr(datetime)').extract_first()
            }