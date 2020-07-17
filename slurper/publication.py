import scrapy
import logging
from scrapy.crawler import CrawlerProcess
#from lxml import etree

'''
Take a publication URL and extract 
- tags
- editors
- authors
- URLs
To run: `scrapy runspider publication.py --nolog`
'''

logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.ERROR
)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Publication(scrapy.Spider):
    name = 'tags'
    start_urls = [
        'https://marker.medium.com/archive',
    ]

    '''
    - Tags
        - Find a header tag that contains "Tags"
        - Find all siblings with an index
        - Find the sibling that contains "Editors". i-1 will bewhere the tags end
    '''
    def parse(self, response):
        tags = self.tags(response)
        editors = self.editors(response)
        writers = self.writers(response)
        print(tags)
        #print(editors)
        #print(writers)


    def writers(self, response):
        writers = {}
        start_selector = response.xpath('//header[descendant::text() = "Writers"]/following-sibling::*') # Start of Editors + following siblings
        # Stop selector not required as there are no non-writer elemtns following the start selector list 
        #stop_selector = response.xpath('//header[descendant::text() = "Writers"]/parent::*')[0] # Start of Writers

        for sibling in start_selector:
            writers[sibling.xpath('./div/a/text()').get()] = sibling.xpath('./div/a/@href').get()

        return writers

    def editors(self, response):
        editors = {}
        start_selector = response.xpath('//header[descendant::text() = "Editors"]/parent::*/following-sibling::*') # Start of Editors + following siblings
        stop_selector = response.xpath('//header[descendant::text() = "Writers"]/parent::*')[0] # Start of Writers

        for sibling in start_selector:
            if stop_selector.get() == sibling.get():
                log.info('Found STOP selector for editors .... stopping')
                break
            else:
                editors[sibling.xpath('.//a/text()').get()] = sibling.xpath('.//a/@href').get()

        return editors


    def tags(self, response) -> dict: 
        tags = {}
        
        start_selector = response.xpath('//header[descendant::text() = "Tags"]/following-sibling::*') # Start of Tags + following siblings
        stop_selector = response.xpath('//header[descendant::text() = "Editors"]/parent::*')[0] # Start of editors

        for sibling in start_selector:
            if stop_selector.get() == sibling.get():
                log.info('Found STOP selector for tags ..... stopping')
                break
            else:
                tags[sibling.xpath('./a/text()').get()] = sibling.xpath('./a/@href').get()

        #tags = {for sibling in start_selector if stop_selector.get() != sibling.get()}
            
        return tags

if __name__ == '__main__':
    process = CrawlerProcess({
        
    })
    process.crawl(Publication)
    process.start()
        









# response.xpath('//section/descendant::text()').getall()
#response.xpath('//header[descendant::text() = "Tags"] | //header[descendant::text() = "Editors"] | //header[descendant::text() = "Writers"]').getall()
