import urllib 
from urllib.parse import urlparse
from dataclasses import dataclass 
from datetime import datetime
from datetime import date
import tldextract 


'''
Module to handle url requests. 
- Parse incoming URL 
- Construct a URL object as shown below 

url:
    - url
    - domain 
    - type: (post, publication)
    - date of processing
    - name of requestor 

'''


@dataclass
class URL:
    url: str
    hostname: str
    domain: str 
    subdomain: str 
    tld: str
    type: str 
    time_requested: datetime 
    requesting_user: str 

class url_parser:

    def parse(self, *urls) -> list:
        ret = []
        urls = list(urls) # Converting to list to access pop 
        urls.reverse() # eversing to maintain order in which user sent the list as this will be reversed back during popping
        print(type(urls), urls)
        while len(urls) > 0:
            #print(urls.pop())
            ret.append(self.process_url(urls.pop()))

        return ret


    def process_url(self, url: str) -> URL:
        extract = tldextract.extract(url)
        subdomain = extract.subdomain
        domain = extract.domain 
        tld = extract.suffix
        hostname = '.'.join(extract[:3])
        type = 'PUB' if subdomain else 'POST'
        time_requested = datetime.now()
        requesting_user = None

        url = URL(url, hostname, domain, subdomain, tld, type, time_requested, requesting_user)

        return url
        


if __name__ == "__main__":

    s1 = "https://marker.medium.com"
    s2 = "https://marker.com"
    url = url_parser().parse(s1, s2)
    print(url)

