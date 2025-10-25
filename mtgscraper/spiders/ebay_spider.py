import scrapy
from datetime import datetime
from mtgscraper.items import MtgCardItem
from urllib.parse import urlencode


class EbayMtgSpider(scrapy.Spider):
    '''
    Spider to scrape Magic: The Gathering card listings from eBay
    '''
    name = 'ebay'
    allowed_domains = ['ebay.com']
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'mtgscraper.pipelines.MtgScraperPipeline': 300,
        }
    }
    
    def __init__(self, card_name=None, max_pages=3, *args, **kwargs):
        super(EbayMtgSpider, self).__init__(*args, **kwargs)
        self.card_name = card_name or 'Black Lotus'
        self.max_pages = int(max_pages)
        self.page_count = 0
        
    def start_requests(self):
        '''
        Generate the initial search URL for eBay
        '''
        search_query = f"mtg {self.card_name}"
        params = {
            '_nkw': search_query,
            '_sop': 12,
            'LH_BIN': 1,
            'LH_ItemCondition': 3000,
        }
        
        base_url = 'https://www.ebay.com/sch/i.html'
        url = f"{base_url}?{urlencode(params)}"
        
        self.logger.info(f"Searching eBay for: {self.card_name}")
        
        # Add extra headers to look more like a real browser
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        yield scrapy.Request(
            url=url, 
            callback=self.parse,
            headers=headers,
            errback=self.errback_httpbin,
            dont_filter=True
        )
    
    def errback_httpbin(self, failure):
        '''
        Handle request failures
        '''
        self.logger.error(f'Request failed: {failure.value}')
        self.logger.warning('eBay may be blocking requests. Try again later or use a VPN.')
    
    def parse(self, response):
        '''
        Parse the search results page
        '''
        self.page_count += 1
        
        # Extract listing items
        listings = response.css('div.s-item__info')
        
        if not listings:
            # Try alternate selectors
            listings = response.css('li.s-item')
        
        for listing in listings:
            item = MtgCardItem()
            
            # Extract card/item name
            title = listing.css('div.s-item__title span::text').get()
            if not title or title.lower() == 'shop on ebay':
                title = listing.css('h3.s-item__title::text').get()
            
            # Extract price
            price_text = listing.css('span.s-item__price::text').get()
            
            # Extract condition
            condition = listing.css('span.SECONDARY_INFO::text').get()
            
            # Extract URL
            url = listing.css('a.s-item__link::attr(href)').get()
            
            # Extract shipping
            shipping = listing.css('span.s-item__shipping::text').get()
            
            # Only yield if we have minimum required data
            if title and price_text:
                item['card_name'] = title.strip()
                item['price'] = price_text.strip()
                item['condition'] = condition.strip() if condition else 'Not specified'
                item['url'] = url
                item['source'] = 'eBay'
                item['timestamp'] = datetime.now().isoformat()
                item['shipping'] = shipping.strip() if shipping else 'See listing'
                item['buy_it_now'] = True
                item['seller'] = 'eBay Seller'
                item['set_name'] = 'Unknown'
                
                yield item
        
        # Follow pagination if within max_pages limit
        if self.page_count < self.max_pages:
            next_page = response.css('a.pagination__next::attr(href)').get()
            if next_page:
                self.logger.info(f"Following pagination: Page {self.page_count + 1}")
                yield response.follow(next_page, callback=self.parse)
