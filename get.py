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

# source url
url = args.url # Sample URL > https://medium.com/series/sample-3d219d98b481
log.info(f'series-url: {url}')

# Medium series object
s = Series()

def get_series(url:str) -> None:
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    #log.debug(soup)
    sections = soup.find_all('section')
    #log.debug(sections)
    for section in sections:
        # Clear attributes and generate mkdwn
        section.attrs = None # Remove attributes of section element
        [make_attr_none(d) for d in section.descendants if d is not bs4.element.NavigableString]
        mkdwn = html2text.html2text(str(section))

        #log.debug(section)
        # Generate Series object
        if section.name == 'section': # This is the title section
            s.name = section.string 
            s.img_url = None # It is not available in the payload
        section_obj = Section()
        s.sections.append(section_obj)
        section_obj.contents = get_contents(section)
        
        #print(mkdwn) # Print to console

# Remove all HTML attributes except for img tags with srcset
# We keep srcset as this has all the image sizes
# Pick the biggest image size (assuming the last image in the srcset is the biggest)
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

'''
Returns:
list of Series -> Section -> Content objects 

Description:
For a given section tag, 
'''
def get_contents(section_tag: bs4.element.Tag):
    # Init contants list to be returned
    contents = []
    # Get dict of img urls keyed by index of section -> div that contains them
    img_dict = get_img_urls(section_tag)
    # Enumerate and iterate over section -> div tags
    for cnt, div in enumerate(section_tag.children):
        # if enumeration counter exists in the img dict, get the list of img
        # urls from the dict, create content objects and append to 
        # section -> contents list
        if cnt in img_dict.keys():
            for i in img_dict[cnt]:
                content = Content()
                content.type = 'img'
                content.text = None
                content.url = i
                contents.append(content)
        # For all text, captions or hrefs, create content objects and append to
        # section -> contents list
        for str in div.strings:
            content = Content()
            content.text = str
            #log.debug(content.text)
            if str.parent.name == 'figcaption': content.type = 'caption'
            elif str.parent.name == 'a': 
                content.type = 'url'
                content.url = str.parent.attrs['href']
            else: content.type = 'text'
            contents.append(content)

    return contents

'''
Returns: 
A dict with key = index of the section -> div (div child of section)
and value = <list> of image urls

Description:
We need to find the index of the section -> divs that contain images so these can 
be inserted back into the contents list of Series -> Section object 

For a given section tag iterate over children (immediate divs)
Filter it by divs that contain an img tag
Get an enumeration to get the index of which first level div under a section
contains an image tag. We will use this index to later insert images back into 
the contents list of a Section object
'''
def get_img_urls(section_tag: bs4.element.Tag) -> dict:
    # dict of section -> divs that contain an image
    img_dict = {i:j for i, j in enumerate(section_tag.children) if j.find('img')}
    # Initialize dict to be returned
    return_dict = {}
    # Filter img_dict, strip everything else but the img urls and add to return_dict
    for k,v in img_dict.items():
        imgs = v.find_all('img')
        img_lst = []
        for i in imgs:
            if i.get('src'):
                img_lst.append(i.get('src'))
            return_dict[k] = img_lst
        
    return return_dict


if __name__ == '__main__':
    get_series(url)
    #print(s.pretty_print_json())
