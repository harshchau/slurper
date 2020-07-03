import requests
import xml.etree.ElementTree as ET 
import html2text
from sys import argv
import logging 
import bs4
from bs4 import BeautifulSoup
import os
import argparse 
from .series import Series, Section, Content

# Logging config 
logging.basicConfig(level = logging.ERROR)
log = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)

# args config 
parser = argparse.ArgumentParser()
parser.add_argument('url', help = 'URL of the medium series', type = str)
parser.add_argument('-j', '--json', help = 'Emit JSON', action = 'store_true')
parser.add_argument('-m', '--markdown', help = 'Emit markdown for each section or post', action = 'store_true')
parser.add_argument('-u', '--uber', help = 'Emite all content as single markdown', action = 'store_true')
args = parser.parse_args()

# source url
url = args.url # Sample URL > https://medium.com/series/sample-3d219d98b481

emit_uber_mkdwn = args.uber    
emit_mkdwn = args.markdown 
emit_json = args.json 

log.info(f'series-url: {url}')



'''
Returns:
Populated Series object

Description:
For a given url, populate the series object and return
'''
def get_series(url:str, emit_uber_mkdwn = False, emit_mkdwn = False, emit_json = False) -> None:
    log.info(f'Emitters: emit-uber-mkdwn={emit_uber_mkdwn}, emit_mkdwn={emit_mkdwn}, emit_json={emit_json}')
    # Medium series object
    s = Series()
    s.sections = []
    # get html string
    html_doc = requests.get(url).text
    # make some soup
    soup = BeautifulSoup(html_doc, 'html.parser')
    # get all sections from the soup
    sections = soup.find_all('section')
    # for all sections, clean html attributes and generate markdown
    for cnt, section in enumerate(sections):
        # Clear attributes and generate mkdwn
        section.attrs = None # Remove attributes of section element
        # Generate Series object values
        if cnt == 0: # This is the title section
            s.name = section.string 
            s.img_url = None # It is not available in the payload
        section_obj = Section()
        # clean out non-required attrs
        [clean_html_attributes(d) for d in section.descendants if d is not bs4.element.NavigableString]
        # Add mkdwn data to sections if emit_mkdwn == True else add ""
        section_obj.mkdwn = (html2text.html2text(str(section))) if emit_mkdwn or emit_uber_mkdwn else ''
        # initialize Series -> Sections
        s.sections.append(section_obj)
        section_obj.contents = get_contents(section) if emit_json else []
    
    # populate uber markdown from markdown 
    s = populate_uber_mkdwn(s) if emit_uber_mkdwn else s
    
    log.debug(f'Series > {s.pretty_print_json()}')
    return s

'''
Returns:
Tag after removing all html attributes except as described below

Description:
Remove all HTML attributes except for img tags with srcset
We keep srcset as this has all the image sizes
Pick the biggest image size (assuming the last image in the srcset is the biggest)
Convert srcset to src because html2text does not work with srcset 
'''
def clean_html_attributes(tag: bs4.element.Tag):
    if tag.name == 'img' or tag.name == 'a': # For img and a tags
        # Get the dict of tag.attrs where attribute is srcset and the parent is a div OR tag is href
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
We need to get a list of content objects which contain text, img, caption and 
href data from the section -> divs
For a given section tag, get the list section -> contents populated with img, 
text, caption and href
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


def populate_uber_mkdwn(series: Series) -> Series:
    m = ''
    for s in series.sections:
        m += s.mkdwn + '-----\n\n' # add horizontal ruler to markdown
        if emit_mkdwn == False: 
            s.mkdwn = ''
            s = []

    if emit_mkdwn == False: series.sections = []
    series.uber_mkdwn = m

    return series 


if __name__ == '__main__':
    s = get_series(url, emit_uber_mkdwn, emit_mkdwn, emit_json)
