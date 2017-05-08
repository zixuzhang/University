#coding=utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from university.items import UniversityItem
from bs4 import BeautifulSoup
import logging

class MySpider(CrawlSpider):
    name = "scu"
    allowed_domains = ['scu.edu.cn']
    # start_urls = ['http://www.scu.edu.cn']
    start_urls = ['http://cpse.scu.edu.cn/news/news-show.php?id=831&type_id=168']
    rules = [Rule(LinkExtractor(), callback='parse_item', follow=True)]

    def parse_item(self, response):
        print '========解析========='
        print u'网页 %s' % response.url
        item = UniversityItem()
        item['url'] = response.url
        if "text/html" in response.headers.get('Content-Type'):
            try:
                content = response.body.decode(response.encoding, 'ignore').encode('utf-8')
                item['html'] = content
            except Exception as e:
                item['html'] = ''
                logging.error('===HTML出错===' + repr(e))
            try:
                text = self.html2text(response.body)
                print len(text)
                item['text'] = text
            except Exception as e:
                item['text'] = ''
                logging.error('===TEXT出错===' + repr(e))
        return item

    def html2text(self,content):
        soup = BeautifulSoup(content, "lxml")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text