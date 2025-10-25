import scrapy


class MtgCardItem(scrapy.Item):
    '''
    Item model for Magic: The Gathering cards
    '''
    card_name = scrapy.Field()
    set_name = scrapy.Field()
    price = scrapy.Field()
    condition = scrapy.Field()
    seller = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    timestamp = scrapy.Field()
    shipping = scrapy.Field()
    buy_it_now = scrapy.Field()
