import requests
import xml.etree.ElementTree as ET 
import html2text
from sys import argv
import logging 
import bs4
from bs4 import BeautifulSoup
import os

log = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def get_series(url:str) -> None:
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    sections = soup.find_all('section')
    for section in sections:
        section.attrs = None
        log.debug(section)
        [make_attr_none(d) for d in section.descendants if d is not bs4.element.NavigableString]
        mkdwn = html2text.html2text(str(section))
        print(mkdwn) # Print to console
        
def make_attr_none(tag):
    if tag.name == 'img': # For img tags
        # Get the dict of tag.attrs where attribute is srcset and the parent is a div
        # We use parent = div to filter out the img tags under noscript
        tag.attrs = {k:v for k,v in tag.attrs.items() if k == 'srcset' and tag.parent.name == 'div'} 
        if('srcset' in tag.attrs): 
            # Rename the srcset key to src
            tag.attrs['src'] = tag.attrs['srcset']
            del tag.attrs['srcset']
            # Convert src values to a list
            a = [tag.attrs['src']]
            a = a[0].split(',') # Split on the ,
            # Split on " " to tokenize the width text such as 500w
            # Take the first element of the sub-array which will be the URL and 
            # discard the width such as 500w
            a = [l.strip().split(' ')[0] for l in a]
            # Pick the last URL, the assumption is that the last URL will be the 
            # largest image
            a = a[-1]
            # Set the src attribute to the last URL
            tag.attrs['src'] = a
    else:
        tag.attrs = None # Remove all attributes
    return tag

if __name__ == '__main__':
    #export_rss() 
    get_series('https://medium.com/series/py-6c6c7d22788f')
