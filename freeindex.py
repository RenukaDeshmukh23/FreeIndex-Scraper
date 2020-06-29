# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request

class FreeindexSpider(scrapy.Spider):
    name = 'freeindex'
    allowed_domains = ['freeindex.co.uk']
    #start_urls = ['https://www.freeindex.co.uk/searchresults.htm?k=food&l=uk']
    term = input("Enter the search term: ")
    #location = input("Enter the location: ")
    start_urls = ['https://www.freeindex.co.uk/searchresults.htm?k='+term+'']
    print(start_urls)

    def parse(self, response):
        names=response.xpath('//*[@class="listing_name"]/a/@href').extract()
        for name in names:
            final_url=response.urljoin(name)
            #yield{'Url':final_url}
            yield Request(final_url,callback=self.parse_info)

        next_page= response.xpath('//a[text()="Next 20 Listings"]/@href').extract_first()
        #if next_page:
            #absolute_next_page = 'https://www.freeindex.co.uk/'+ next_page
        print("working")
        absolute_next_page=response.urljoin(next_page)
        yield Request(absolute_next_page)



    def parse_info(self,response):
        Name=response.xpath('//h1/text()').extract()
        Rating=response.xpath('//*[@class="ratinglarge pull-left"]/@title').extract()
        Address=response.xpath('//*[@class="psummary_company"]/text()').extract()
        Website=response.xpath('//*[@style="display:flow-root;"]//a/@title').extract()
        Keywords=response.xpath('//*[@class="DescItem"]//a/text()').extract()

        yield{'Keywords':Keywords,
                'Name':Name,
                'Rating':Rating,
                'Address':Address,
                'Website':Website}





        #next_page = response.xpath('//*[@class="boxlink"]/@href[text()="Next 20 Listings"]').extract()
