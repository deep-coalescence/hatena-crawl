import scrapy
import re

def isblocked(url):
    return 'b.hatena' in url or '/s/' in url or '/www' in url

class HatenaSpider(scrapy.Spider):
    name = 'hatena'
    allowed_domains = ['hatenablog.com','hatenablog.jp','hatenadiary.com', 'hatenadiary.jp', 'hateblo.jp']
    start_urls = ['http://hatenablog.com/']

    custom_settings = {
        # 'DEPTH_LIMIT': 10,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
    }

    def parse(self, response):
        from_url = response.request.url
        if re.match(r'.+/entry/.+$', from_url):
            # then we crawl
            if response.xpath("//article"):
                yield {
                    'url': from_url,
                    'title': response.xpath("//h1[@class='entry-title']/a/text()").get(),
                    'body': (response.xpath("//article/div/div[contains(@class,'entry-content hatenablog-entry')]") or response.xpath("//article/div/div[contains(@class,'entry-content')]")).get(),
                }
        for topic_links in response.xpath("//a[starts-with(@href, 'https://hatenablog.com/topics/')]/@href").getall():
            if not isblocked(topic_links):
                yield response.follow(topic_links, self.parse)
        for entry_links in response.xpath("//a[contains(@href, '/entry/')]/@href").getall():
            if not isblocked(entry_links):
                yield response.follow(entry_links, self.parse)
        for entry_links in response.xpath("//a[contains(@href, '/archive/')]/@href").getall():
            if not isblocked(entry_links):
                yield response.follow(entry_links, self.parse)