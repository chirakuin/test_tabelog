# http://amacbee.hatenablog.com/entry/2016/12/01/210436
# docker run -p 8050:8050 scrapinghub/splash


import re
import time
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from selenium import webdriver

from testproject_02.items import Contents

from scrapy_splash import SplashRequest

class Tabelog_02Spider(scrapy.Spider):
    name = 'tabelog_02'
    allowed_domains = ['tabelog.com']
    # start_urls = ['http://tabelog.com/tokyo/rstLst/lunch/?LstCosT=2&RdoCosTp=1']
    start_urls = ['https://tabelog.com/tokyo/rstLst/{}/'.format(str(i)) for i in range(1, 2)]

    # rules = [
    #     Rule(LinkExtractor(allow=r'/A\d+/A\d+/\d+/$'), callback='parse_restaurant'),
    # ]

#response.css('#column-main > div.js-rstlist-info.rstlist-info > div:nth-child(2) > div.list-rst__wrap.js-open-new-window > div.list-rst__header > div > div > h4 > a')
#response.css('div.list-rst__wrap.js-open-new-window > div.list-rst__header > div > div > h4 > a::('href')).xpath('string()').get().strip()

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_01, args={'wait': 0.5})

            # yield SplashRequest(self.start_urls[0], self.parse,
            #     args={'wait': 0.5},
            # )

#column-main > div.js-rstlist-info.rstlist-info > div:nth-child(3) > div.list-rst__wrap.js-open-new-window > div.list-rst__header > div > div.list-rst__rst-name-wrap > h4 > a
#column-main > div.js-rstlist-info.rstlist-info > div:nth-child(4) > div.list-rst__wrap.js-open-new-window > div.list-rst__header > div > div > h4 > a
# response.xpath('/html/body/div[21]/div[1]/div[7]/div[6]/div[1]/div[2]/div[1]/div/div/h4/a/@href').getall()
#column-main > div.rstdtl-rvwlst > div:nth-child(19) > div.rvw-item__contents.u-clearfix > div.js-rvw-item-wrapper > div > a
    def parse_01(self, response):
        urls = response.css('a::attr("href")').re('https://tabelog.com/tokyo/A\d+/A\d+/\d+/$')
        for url in urls:
            yield SplashRequest(url, self.parse_02, args={'wait': 0.5})

    def parse_02(self, response):
        urls = response.css('#rdnavi-review > div > a::attr("href")').re('https://tabelog.com/tokyo/A\d+/A\d+/\d+/dtlrvwlst/$')
        for u in urls:
            for n in range(1, 2):
                url = u + 'COND-0/smp1/?smp=1&lc=0&rvw_part=all&PG=' + str(n)
                print(url)
                yield scrapy.Request(url, callback=self.parse_contents)

    def parse_contents(self, response):
        _url = response.request.url
        driver = webdriver.Chrome()
        driver.get(_url)
        time.sleep(3)
        

        #column-main > div.rstdtl-rvwlst > div:nth-child(9) > div.rvw-item__contents.u-clearfix > div.js-rvw-item-wrapper > div > a
        for n in range(0, 30):
            try:
                driver.find_element_by_css_selector('div.rstdtl-rvwlst > div:nth-child(' + str(n) + ') > div.rvw-item__contents.u-clearfix > div.js-rvw-item-wrapper > div > a').click()
                time.sleep(0.5)
            except Exception as e:
                print(n)
                print(e)
                
        time.sleep(1)
        # body = driver.find_element_by_xpath('/html/body/div[13]/div[1]/div/div[4]/div[1]/div[2]').text
        try:  
            if driver.find_element_by_xpath('/html/body/div[13]/div[1]/div/div[4]/div[1]/div[2]').text:
                body = driver.find_element_by_xpath('/html/body/div[13]/div[1]/div/div[4]/div[1]/div[2]').text
            else: 
                # driver.find_element_by_xpath('/html/body/div[13]/div[1]/div/div[4]/div[1]/div[1]/div[' + str(i) + ']').text:
                body = driver.find_element_by_xpath('/html/body/div[13]/div[1]/div/div[4]/div[1]/div[1]').text
        except Exception as e:
            print('*****************************************')
            print(n)
            print(e)

        _url = response.request.url
        _url = re.sub(r'dtlrvwlst.*', '' , _url)
        print('#########################################')
        print(body)
        item = Contents(
            name = driver.find_element_by_xpath('/html/body/div[13]/div[1]/div/div[2]/div[1]/section/div[1]/div[1]/div/h2/a').text,
            url = _url,
            body = body,
            # attr = attr,
            # star_dinner = star_dinner,
            # star_lunch = star_lunch,
            # price_dinner = price_dinner,
            # price_lunch = price_lunch,
            # times = times,
            # day = day,
            # title = title,
            # body = body
        )

        driver.quit()
        print(item)
        time.sleep(1)
        yield item
