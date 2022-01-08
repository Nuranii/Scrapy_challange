import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
import re
from property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        for i in range(1,3):
            url = response.url+'&pageset='+str(i)
            yield Request(url,callback=self.pages)

    def pages(self,response):
        links = response.css('.h4-space a::attr(href)').extract()  
        for link in links:
            yield Request('https://londonrelocation.com'+link,callback=self.parse_page) 

        
    def parse_page(self,response):

        title = response.css('h1::text').get()
        price = response.css('h3::text').get()
        link = response.url

        price = (re.findall("\d+", price))[0] 

        property = ItemLoader(item=Property()) 
        property.add_value('title', title) 
        property.add_value('price',price ) 
        property.add_value('link',''+link )
        return property.load_item() 

