# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

from w3lib.html import remove_tags


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value+"-jobbole"


def get_nums(value):
    return int(value)


def return_value(value):
    return value


def handle_jobaddr(value):
    add_list = value.split('\n')
    add_list = [item.strip() for item in add_list if item.strip() != '查看地图']
    return "".join(add_list)


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(add_jobbole, lambda x: x+'bobby'),
    )
    create_time = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into jobbole_article(`title`, `create_time`, `praise_nums`, `url`, `url_object_id`, \
                            `front_image_url`, `front_image_path`, `content`) VALUES ('%s', '%s', %d, '%s', '%s', '%s', '%s', '%s')" \
                     % (self['title'], self['create_time'], self['praise_nums'], self['url'],
                        self['url_object_id'], self['front_image_url'][0],
                        self['front_image_path'], self['content'])
        return insert_sql


class ZhihuQestionItem(scrapy.Item):
    # 知乎问题item
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    question_id = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into zhihu_question..."  # 需要进一步完善
        return insert_sql


class ZhihuAnswerItem(scrapy.Item):
    # 知乎answer item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()


class LagouJobItem(scrapy.Item):
    # 拉钩网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field()
    work_years = scrapy.Field()
    degree_need = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )

    def get_insert_sql(self):
        insert_sql = "insert into lagou_table..."  # 需要进一步完善
        return insert_sql


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()
