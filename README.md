# pixiv_crawl

基于Scrapy 的 PIXIV爬虫，功能简单（简陋），实现了简单的页面信息抽取，JSON API信息抽取，IMAGE存储等功能。
基于Scrapy的配置文件进行灵活配置（包含某些福利选项），并通过Cookie Middleware实现模拟登录等功能。



用户配置信息：
* IMAGES_STORE 配置图片存储的地址
* PIXIV_USER_NAME 配置你的PIXIV用户名
* PIXIV_USER_PASS 配置你的PIXIV密码
* START_DATE 抓取的时间
* __SELECT_MODE_IDX__ 热榜模式选择
