# Scrapy settings for mtgscraper project
#
# This configuration follows web scraping best practices:
# 1. Respects robots.txt (ethical scraping)
# 2. Uses realistic User-Agent (mimics real browser)
# 3. AutoThrottle enabled (adapts to server load)
# 4. Rate limiting and delays (avoids overwhelming servers)
# 5. Limited concurrency (respectful behavior)
#
# For production use, consider adding:
# - Rotating proxies middleware
# - User-Agent rotation
# - CAPTCHA solving integration

BOT_NAME = 'mtgscraper'

SPIDER_MODULES = ['mtgscraper.spiders']
NEWSPIDER_MODULE = 'mtgscraper.spiders'

# Crawl responsibly by identifying yourself (looks like real Chrome browser)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Obey robots.txt rules - IMPORTANT: Always respect website policies
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests (keep low to be respectful)
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Configure delays for requests - mimic human browsing speed
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# AutoThrottle - automatically adjusts crawling speed based on server load
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Enable cookies (helps with eBay)
COOKIES_ENABLED = True

# Retry settings
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Disable Telnet Console
TELNETCONSOLE_ENABLED = False

# Override the default request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'mtgscraper.middlewares.CaptchaSolverMiddleware': 585,
    'mtgscraper.middlewares.ProxyMiddleware': 590,
}

# Splash Settings (optional - only if using Splash)
SPLASH_URL = 'http://localhost:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Set settings whose default value is deprecated
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'
