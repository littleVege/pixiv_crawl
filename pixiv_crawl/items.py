# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PixivCrawlItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    img_urls = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    rank = scrapy.Field()
    yes_rank = scrapy.Field()
    total_score = scrapy.Field()
    views = scrapy.Field()
    is_sexual = scrapy.Field()
    illust_id = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    image_paths = scrapy.Field()
