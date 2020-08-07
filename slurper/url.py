from dataclasses import dataclass 
from datetime import datetime
from datetime import date
import datetime as import_datetime
import tldextract 
from json import JSONEncoder
import requests
from reppy.robots import Robots
from validator_collection import validators, checkers, errors
from .utils import dynamodb
import time
import json
import random 
from datetime import timezone


'''
Module to handle url requests. 
- Parse incoming URL 
- Construct a URL object as shown below 

'''



@dataclass
class Url:
    url: str
    scheme: str 
    hostname: str
    domain: str 
    subdomain: str 
    suffix: str
    url_type: str 
    time_requested: int  
    requesting_user: str 
    ttl: int 

class UrlProcessor:

    '''
        For the list of provided urls pop each url in order and send to process_url
    '''
    def parse(self, *urls) -> list:
        ret = {}
        parsed_urls = []
        error_urls = []
        ignored_urls = [] # URL's we won't be processing even if they are valid 
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
            u = urls.pop()
            try:
                if self.is_valid(u) is True:
                    u = self.process_url(u)
                    if u.url_type == 'PUB':
                        parsed_urls.append(u)
                    else:
                        ignored_urls.append(u)
                else:
                    pass 
            except (errors.EmptyValueError, errors.CannotCoerceError, errors.InvalidURLError) as err:
                error_urls.append(u)
                print(err)

        ret['parsed_urls'] = parsed_urls
        ret['error_urls'] = error_urls
        ret['ignored_urls'] = ignored_urls
        return ret

    '''
        For each url
            check against robots.txt 
            extract various parts
    '''
    def process_url(self, url: str) -> Url:
        extract = tldextract.extract(url)
        # Find the first non None part in the url and do a substring on the url from index 0 - whatever
        scheme = url[:url.index([part for part in extract if part][0])]
        subdomain = extract.subdomain
        domain = extract.domain 
        suffix = extract.suffix
        hostname = '.'.join(part for part in extract if part)
        url_type = 'PUB' if (domain == 'medium' and subdomain != '' and subdomain != 'www') else 'UNKNOWN' # Process only medium publications for now
#        time_requested = datetime.now().strftime("%A, %d, %B %Y %I:%M:%S %p")
#        ttl = (datetime.strptime(time_requested, "%A, %d, %B %Y %I:%M:%S %p") + import_datetime.timedelta(0,self.ttl_delta(),0,0,0,0,0)).strftime("%A, %d, %B %Y %I:%M:%S %p")
        time_requested = int(datetime.now().timestamp())
#        print('#####', time_requested, type(time_requested))
        ttl = time_requested + self.ttl_delta()
        print('#####', ttl)
        requesting_user = None

        url = Url(url, scheme, hostname, domain, subdomain, suffix, url_type, time_requested, requesting_user, ttl)

        return url

    def is_valid(self, url: str) -> bool:
        ret = False
        try:
            ret = True if validators.url(url) else False
        except (errors.EmptyValueError, errors.CannotCoerceError, errors.InvalidURLError) as err:
            raise err

        return ret 
    
    def can_crawl(self, url: str) -> bool:
        ret = False
        robots_url = Robots.robots_url(url)
        robots = Robots.fetch(robots_url, headers={'user-agent': 'slurper'})
        ret = robots.allowed(url, 'slurper')
        return ret

    def ttl_delta(self) -> int:
        return random.randrange(0,10)
    
class UrlEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
        


if __name__ == "__main__":

    s1 = "https://marker.medium.com"
    s2 = "https://medium.com"
    s3 = "https://www.google.com"
    s4 = "https://www.medium.com"
    s5 = 'https://d.medium.com'
    l = []
    l.append(s1)
    l.append(s2)
    l.append(s3)
    l.append(s4)
    l.append(s5)
    urls = UrlProcessor().parse(l)
    print(json.dumps(urls, cls=UrlEncoder, indent=2))

    util = dynamodb.DBUtils()
    util.upsert_urls(urls)
    
