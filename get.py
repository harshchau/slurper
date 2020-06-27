import requests
import xml.etree.ElementTree as ET 
import html2text
from sys import argv
import logging 
import bs4
from bs4 import BeautifulSoup
import os
import argparse 
from series import Series, Section, Content

# Logging config 
logging.basicConfig(level = logging.ERROR)
log = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)

# args config 
parser = argparse.ArgumentParser()
parser.add_argument('url', help = 'URL of the medium series', type = str)
args = parser.parse_args()

url = args.url # Sample URL > https://medium.com/series/sample-3d219d98b481
log.info(f'series-url: {url}')

# Medium series object
s = Series()

def get_series(url:str) -> None:
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    sections = soup.find_all('section')
    #print(sections)
    for section in sections:
        # Clear attributes and generate mkdwn
        section.attrs = None # Remove attributes of section element
        [make_attr_none(d) for d in section.descendants if d is not bs4.element.NavigableString]
        mkdwn = html2text.html2text(str(section))

        # Generate Series object
        if section.name == 'section': # This is the title section
            s.name = section.string 
            s.img_url = None # It is not available in the payload
        section_obj = Section()
        s.sections.append(section_obj)
        section_obj.contents = get_contents(section)
        #log.debug(section)
        
        #print(mkdwn) # Print to console

# Remove all HTML attributes except for img tags with srcset
# We keep srcset as this has all the image sizes
# Convert srcset to src because html2text does not work with srcset 
def make_attr_none(tag):
    if tag.name == 'img' or tag.name == 'a': # For img and a tags
        # Get the dict of tag.attrs where attribute is srcset and the parent is a div
        # We use parent = div to filter out the img tags under noscript
        tag.attrs = {k:v for k,v in tag.attrs.items() if (k == 'srcset' and tag.parent.name == 'div') or (k == 'href')} 
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


def get_contents(section_tag: bs4.element.Tag):
    contents = []
    s = [ str for str in section_tag.strings]
    for str in s:
        content = Content()
        content.text = str
        if str.parent.name == 'figcaption': content.type = 'caption'
        else: content.type = 'text'
        contents.append(content)

    return contents


if __name__ == '__main__':
    get_series(url)
    print(s.pretty_print_json())
