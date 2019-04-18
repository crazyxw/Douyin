# -*- coding: utf-8 -*-

# Scrapy settings for Douyin project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Douyin'

SPIDER_MODULES = ['Douyin.spiders']
NEWSPIDER_MODULE = 'Douyin.spiders'
DOWNLOAD_DELAY = 1
COOKIES_ENABLED = False
ROBOTSTXT_OBEY = False

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
   # 'Douyin.middlewares.DouyinSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
   # 'Douyin.middlewares.DouyinDownloaderMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPLASH_URL = "http://localhost:8050"
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'