from dataclasses import dataclass 
from datetime import datetime
from datetime import date
import tldextract 
from json import JSONEncoder
import requests
from reppy.robots import Robots


'''
Module to handle url requests. 
- Parse incoming URL 
- Construct a URL object as shown below 

'''



@dataclass
class URL:
    url: str
    scheme: str 
    hostname: str
    domain: str 
    subdomain: str 
    suffix: str
    url_type: str 
    time_requested: datetime 
    requesting_user: str 

class UrlProcessor:

    '''
        For the list of provided urls pop each url in order and send to process_url
    '''
    def parse(self, *urls) -> list:
        ret = []
        #print('>>>>>', type(urls[0]))
        if(type(urls[0])) is not list:
            urls = list(urls) # Converting to list to access pop 
        else:
            urls = urls[0]
        #print('>>>>>', urls)
        urls.reverse() # eversing to maintain order in which user sent the list as this will be reversed back during popping
        #print(type(urls), urls)
        while len(urls) > 0:
            #print(urls.pop())
            ret.append(self.process_url(urls.pop()))

        return ret

    '''
        For each url
            check against robots.txt 
            extract various parts
    '''
    def process_url(self, url: str) -> URL:
        extract = tldextract.extract(url)
        # Find the first non None part in the url and do a substring on the url from index 0 - whatever
        scheme = url[:url.index([part for part in extract if part][0])]
        subdomain = extract.subdomain
        domain = extract.domain 
        suffix = extract.suffix
        hostname = '.'.join(part for part in extract if part)
        url_type = 'PUB' if subdomain else 'POST'
        time_requested = datetime.now().timestamp() * 1000
        requesting_user = None

        url = URL(url, scheme, hostname, domain, subdomain, suffix, url_type, time_requested, requesting_user)

        return url

    def can_crawl(self, url: str) -> bool:
        ret = False
        robots_url = Robots.robots_url(url)
        robots = Robots.fetch(robots_url, headers={'user-agent': 'slurper'})
        ret = robots.allowed(url, 'slurper')
        return ret
    
class SeriesEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
        


if __name__ == "__main__":

    s1 = "https://marker.medium.com"
    s2 = "https://medium.com"
    l = []
    l.append(s1)
    l.append(s2)
    url = UrlProcessor().parse(l)
    print(SeriesEncoder().encode(url))

