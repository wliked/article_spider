# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # 收集伯乐在线所有404的url以及404页面数
    handle_httpstatus_list = [404]

    def __init__(self):
        self.fail_urls = []
        self.browser = webdriver.Chrome(executable_path="/home/drjr/chromedriver/chromedriver")
        super(JobboleSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider, reason):
        print("spider closed")
        self.browser.quit()

    def parse(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")  # 将scrapy数据收集器中的变量增1

        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)

        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)

    def parse_detail(self, response):
        # article_item = JobBoleArticleItem()
        #
        # front_image_url = response.meta.get("front_image_url", "")
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()'
        #                                       ).extract()[0].strip().replace("·", '').strip()
        # praise_nums = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0])
        # # fav_nums = int(re.match(r".*(\d+).*", response.xpath("//span[contains(@class, 'bookmark-btn')]/text()"
        # #                                                      ).extract()[0]).group(1))
        #
        # content = response.xpath("//div[@class='entry']").extract()[0]
        #
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["front_image_url"] = [front_image_url]
        # article_item["front_image_path"] = ''
        # article_item["title"] = title
        # try:
        #     create_time = datetime.datetime.strptime(create_time, "%Y/%m/%d")
        # except Exception as e:
        #     create_time = datetime.datetime.now()
        #
        # article_item["create_time"] = create_time
        # article_item["praise_nums"] = praise_nums
        # article_item["content"] = content

        # print(title)

        # 通过itemtloader 加载item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # item_loader.add_css("title", "")
        item_loader.add_xpath("title", '//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath("create_time", '//p[@class="entry-meta-hide-on-mobile"]/text()')

        item_loader.add_xpath("praise_nums", "//span[contains(@class, 'vote-post-up')]/h10/text()")
        item_loader.add_xpath("content", "//div[@class='entry']")

        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_value("front_image_path", '')

        article_item = item_loader.load_item()

        yield article_item

        pass
