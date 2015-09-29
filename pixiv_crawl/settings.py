# -*- coding: utf-8 -*-

# Scrapy settings for pixiv_crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import datetime

BOT_NAME = 'pixiv_crawl'

SPIDER_MODULES = ['pixiv_crawl.spiders']
NEWSPIDER_MODULE = 'pixiv_crawl.spiders'

ITEM_PIPELINES = {
    'pixiv_crawl.pipelines.PixivImagesPipeline': 1,
    'pixiv_crawl.pipelines.PixivMetaPipeline': 10
  }

LOG_LEVEL = "ERROR"

DOWNLOAD_DELAY = 1
COOKIES_ENABLED = True
# COOKIES_DEBUG = True
IMAGES_STORE = '/your/path/to/save/imgs/'	#用于保存图片的地址，最后需要加上/

#########USER INFO
PIXIV_USER_NAME = 'username'	#在此设置登录用户名
PIXIV_USER_PASS = 'password'	#在此设置登录密码
#########HOST INFO
START_DATE = datetime.date(2015,9,1)    #在此设置开始时间
#########PXIIV_MODE
__PIXIV_MODES__ = [
    'daily',        #0 每日热榜
    'weekly',       #1 每周热榜
    'monthly',      #2 每月热榜
    'male',         #3 男性关注
    'female',       #4 女性关注
    'daily_r18',    #5 福利
    'weekly_r18',   #6 福利
    'male_r18',     #7 福利
    'female_r18'    #8 福利
]
__SELECT_MODE_IDX__ = 6 #在此设置对应索引号
SELECT_MODE = __PIXIV_MODES__[__SELECT_MODE_IDX__]  #无需设置，自动生成，供程序使用
########GENERATE IMAGE STORE
IMAGES_STORE = IMAGES_STORE + '{mode}/{year}{month}{day}'.format(
                        year=START_DATE.year,
                        month=str(START_DATE.month).zfill(2),
                        day=str(START_DATE.day).zfill(2),
                        mode = SELECT_MODE
                )

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pixiv_crawl (+http://www.yourdomain.com)'
