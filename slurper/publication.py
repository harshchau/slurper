import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import logging
import argparse
from bs4 import BeautifulSoup
import time
from url import UrlProcessor
from urllib.parse import urlparse
from dataclasses import dataclass
import boto3
import datetime
#import chromedriver_binary # adds chromedriver_binary to the PATH

'''
Use a headless browser to navigate a series or post and get the entire dataset
Steps:
    # Set up headless browser
    # Get initial dataset
    # Click on last element to get the next 
    # Add the newly received element to the initial dataset 
    # Repeat 
'''

# args config 
#parser = argparse.ArgumentParser()
#parser.add_argument('-url', help = 'URL of the medium series', type = str)
#args = parser.parse_args()

# source url
#url = args.url # Sample URL > https://medium.com/series/sample-3d219d98b481

#if url is None: url = 'https://medium.com/series/sample-3d219d98b481'

# Logging config 
logging.basicConfig(level = logging.ERROR)
log = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)

class PublicationProcessor:

    # Set up headless browser 
    chrome_options = webdriver.ChromeOptions() 
#    chrome_options.add_argument("--headless") 
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    chrome_options.headless = True 
#    chrome_options.binary_location = '/var/task/lib/headless-chromium'
#    browser = webdriver.Chrome(options=chrome_options,executable_path='/Users/harsh/git/slurper/slurper-env/lib/python3.8/site-packages/chromedriver_binary/chromedriver')
    browser = webdriver.Chrome(options=chrome_options)

    # Get initial dataset 
    def get_initial_payload(self, url: str):
        log.debug(f'URL > {url}')
        self.browser.get(url)
        elements = self.browser.find_elements_by_tag_name('section')
        #log.debug(f'Found {len(elements)} elements')

        return elements

    def iterate_a(self, element_list: list, text_element_list: list = []) -> list:
        if element_list[-1] == element_list[-2]: 
            #log.debug(f'ENDING ..... found {len(element_list)} elements')

            # Drop the last element before returning because when the else reaches 
            # the end of the content, it still add the last element to the 
            # element_list. In other words, we will add the last element to the 
            # list and then compare to previous element in the next step. This 
            # comparison then tells us whether or not thr elements are equal
            return element_list[:-1], text_element_list[:-1]
        else:
            log.debug(len(element_list))
            self.click(element_list[-1])
            element_list.append(self.browser.find_elements_by_tag_name('section')[-1])
            text_element_list.append(self.get_element_as_text(element_list[-1]))

            return self.iterate_a(element_list, text_element_list)

    def click(self, element):
        #e = element.find_elements_by_tag_name('div')[-1]
        #action = ActionChains(browser)
        #action.move_to_element(e).click().perform()
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)

    def get_element_as_text(self, element):
        s = None
        try:
            s = element.get_attribute('outerHTML')
        except selenium.common.exceptions.StaleElementReferenceException as error:
            # Just log and don't take action as the text for stale elements has been
            # captured in the text_element list 
            log.error(f'IGNORE > {error.msg}')

        return s

    def get_urls(self, text_elements: list) -> list:
        ret = []
        for e in text_elements:
            soup = BeautifulSoup(e, 'html.parser')
            for a in soup.find_all('a'):
                ret.append(a['href'])
        return ret 

    def remove_author_urls(self, urls_list: list) -> list:
        ret = []
        up = UrlProcessor
        for u in urls_list:
            #url_parts = up.process_url(u)
            #print(u[u.index(url_parts.suffix):])
            path = urlparse(u).path
            if path[1:].startswith('@'): continue # Don't add user URL's
            ret.append(u)

        return ret  

    def get_post_urls(self, url: str): 
        elems = self.get_initial_payload(url)
        text_elements = [self.get_element_as_text(e) for e in elems]
        #log.info(f'Found {len(elems)} elements on inital run')
        elems, text_elements = self.iterate_a(elems, text_elements)
        #log.info(f'Found {len(text_elements)} elements and {len(elems)} text elements')
        #log.info(text_elements[0])
        #urls = set(get_urls(text_elements) ) # Remove duplicates
        urls = []
        [urls.append(x) for x in self.get_urls(text_elements) if x not in urls] # Remove duplicates this way to maintain order of urls
        urls = self.remove_author_urls(urls)
        #for u in urls:
        #    log.info(u)
        #log.debug(f'{len(urls)} urls found')

        return urls

if __name__ == '__main__':
    #url = 'https://medium.com/series/sample-3d219d98b481'
    url = 'https://marker.medium.com'
    p = PublicationProcessor()
    urls = p.get_post_urls(url)
    for u in urls:
        log.info(u)
    log.info(type(urls))
    log.info(len(urls))