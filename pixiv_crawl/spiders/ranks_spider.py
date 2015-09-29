# coding=utf-8
__author__ = 'littleVege'
import scrapy
import json
import datetime
from pixiv_crawl.items import PixivCrawlItem
from scrapy.exceptions import *
class PixivSpider(scrapy.Spider):
    name = "pixiv_daily_ranking"
    allowed_domains = ['pixiv.net']

    """开始抓取，首先通过登录页进行登录，并保存和跟踪COOKIE"""
    def start_requests(self):
        setting = self.settings
        if not setting['PIXIV_USER_NAME'] or not setting['PIXIV_USER_PASS']:
            raise CloseSpider('username or password error!!!')
        return [
            scrapy.FormRequest(url = 'https://www.secure.pixiv.net/login.php',
                               formdata = {
                                   'pixiv_id':setting['PIXIV_USER_NAME'],
                                   'pass':setting['PIXIV_USER_PASS'],
                                   'skip':'1',
                                   'mode':'login'
                               },
                               callback = self.logged_in)
                ]

    """登录完成后操作，
    判断是否成功，成功则生成当天的首个LIST页，用户名错误则关闭爬虫
    """
    def logged_in(self,response):
        if response.url == 'https://www.secure.pixiv.net/login.php':
            raise CloseSpider('username or password error!!!')
        yield scrapy.Request(self.generate_list_url(self.settings['START_DATE']),callback=self.parse)

    """
    解析列表页
    列表页内容为一个JSON字符串
    Example:

        {
            content: "all"
            contents: [
                {illust_id: 52746276, title: "あっくんとカノジョ２９", width: 677, height: 800, date: "2015年09月27日 20:20",…}
                ,…
                ]
            date: "20150927"
            mode: "daily"
            next: 3
            next_date: null
            page: "2"
            prev: 1
            prev_date: "20150926"
            rank_total: 500
        }
    """
    def parse(self, response):
        result = json.loads(response.body, 'utf8')
        for section in result['contents']:
            item = PixivCrawlItem()
            item['title'] = section['title']
            item['date'] = section['date']
            item['user_id'] = section['user_id']
            item['user_name'] = section['user_name']
            item['rank'] = section['rank']
            item['yes_rank'] = section['yes_rank']
            item['total_score'] = section['total_score']
            item['views'] = section['view_count']
            item['is_sexual'] = section['illust_content_type']['sexual']
            item['illust_id'] = section['illust_id']
            item['tags'] = section['tags']

            # header中不写referer或者referer正确会导致403错误。
            yield scrapy.Request(
                self.generate_detail_url(section['illust_id']),
                callback=self.parse_detail,
                meta={'item':item},
                headers={
                    'referer': response.url,
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
                }
            )
        if result['next']:
            url = self.generate_list_url(self.settings['START_DATE'], result['next'],self.settings['SELECT_MODE'])
            yield scrapy.Request(url, callback=self.parse)

    """解析详情页，提取出其中的大图"""
    def parse_detail(self, response):
        item = response.meta['item']
        item['url'] = response.url
        img_url = response.css('._illust_modal img').css('::attr("data-src")').extract()
        if (len(img_url) > 0):
            item['img_urls'] = img_url
        yield item

    """ 根据给定的illust_id返回对应的详情页URL
    Args:
        illust_id:每个绘画的唯一ID号
    Returns:
        根据模板生成的URL地址字符串
    """
    def generate_detail_url(self, illust_id):
        return 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'.format(illust_id)

    """根据给定的时间参数，生成对应的时间字符串"""
    def str_date(self,date=datetime.date.today()):
        return '{year}{month}{day}'.format(year=date.year,month=str(date.month).zfill(2),day=str(date.day).zfill(2))

    """ 根据给定的时间和页码，生成对应的列表页地址
    Args:
        date:时间，默认值为当天
        page:页码，默认值为1
    Returns:
        列表页API的URL地址字符串
    """
    def generate_list_url(self, date=datetime.date.today(), page=1, mode = 'daily'):
        url_tmpl = 'http://www.pixiv.net/ranking.php?mode={mode}&date={str_date}&p={page}&format=json'
        if (isinstance(date, datetime.date)):
            str_date = self.str_date(date)
        else:
            str_date = date
        return url_tmpl.format(str_date = str_date, page = page,mode = mode)
