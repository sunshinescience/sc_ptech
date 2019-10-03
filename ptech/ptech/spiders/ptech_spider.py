import scrapy
from ptech.items import PtechItem

class PtechSpider(scrapy.Spider):
    name = 'petrol_tech'
    allowed_domains = ["onepetro.org"]

    # Obtain start_urls list
    start_urls = []
    volume_href = [
                'https://www.onepetro.org/journals/Journal%20of%20Petroleum%20Technology'
                ]
    volume_num = 71
    active_issue_nums = range(8, 0, -1)
    issue_nums = range(12, 0, -1)
    for i in volume_href:
        for j in active_issue_nums:
            next_page = i + '/' + str('{:02}'.format(volume_num)) + '/' + str('{:02}'.format(j))
            start_urls.append(next_page)     
        for volume in range(70, 0, -1):
            for issue in issue_nums:
                next_pages = i + '/' + str('{:02}'.format(volume)) + '/' + str('{:02}'.format(issue))
                start_urls.append(next_pages)

    def parse(self, response):
        for href in response.xpath('//h3[@class="book-title"]//a/@href'):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_abstracts)
        
        # Obtain the next page to obtain links for abstracts from that
        for href in response.xpath('//ul[@class="toggle-section open"]//li/a/@href'):
            next_page_url = href.extract()
            yield scrapy.Request(next_page_url) 
        
    def parse_abstracts(self, response):
        item = PtechItem()

        try:
            item['abstract'] = (response.xpath('//div[@class="abstract"]//p/text()').extract())[1:]
            item['source'] = response.xpath('//div[@class="highlighted"]//dd[5]//text()').extract_first()
            item['volume'] = response.xpath('//div[@class="highlighted"]//dd[6]//text()').extract_first()
            item['issue'] = response.xpath('//div[@class="highlighted"]//dd[7]//text()').extract_first()
            item['publication_date'] = response.xpath('//div[@class="highlighted"]//dd[8]//text()').extract_first()
            item['title'] = (response.xpath('//h1[@class="document-title"]/text()').extract_first()).strip()
        except:
            pass

        yield item

    
 