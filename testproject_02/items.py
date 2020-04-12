import scrapy


class  Contents(scrapy.Item):

    name = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()

    # user = scrapy.Field()
    # attr = scrapy.Field()
    # star_dinner = scrapy.Field()
    # star_lunch = scrapy.Field()
    # price_dinner = scrapy.Field()
    # price_lunch = scrapy.Field()
    # times = scrapy.Field()
    # day = scrapy.Field()
    # title = scrapy.Field()