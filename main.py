# coding:utf-8

from scrapy import cmdline

# 启动全部爬虫
# cmdline.execute('scrapy crawlall'.split())


# cmdline.execute('scrapy crawl swjtu'.split())
cmdline.execute('scrapy crawl scu -L ERROR'.split())
# cmdline.execute('scrapy crawl scu'.split())