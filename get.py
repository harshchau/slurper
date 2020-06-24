import requests
import xml.etree.ElementTree as ET 
import html2text
from sys import argv
import logging 
from bs4 import BeautifulSoup

def loadRSS(url):
    resp = requests.get(url)
    return resp

def getRssItems(rssURL) -> dict:
    ns = {'dc': 'http://purl.org/dc/elements/1.1/', 
            'content': 'http://purl.org/rss/1.0/modules/content/'
        }
    posts = {}
    tree = ET.fromstring(loadRSS(rssURL).text)
    for item in tree.iter('item'):
        try:
            title = item.find('title').text
            content = item.find('content:encoded', ns)
            posts[title] = html2text.html2text(content.text)
        except Exception as e:
            logging.error(f'Error in title: {title} | Error message: {e}', exc_info = True)
    
    return posts

def exportRss():
    url = 'https://medium.com/feed/@'
    try:
        user_name = argv[1]
    except IndexError:
        user_name = input('Enter a username > ')
    
    mkdwn = ''
    posts = getRssItems(url + user_name)
    for title, content in posts.items():
        mkdwn += '#' + title + '\n\n' + content
    
    print(mkdwn)

if __name__ == '__main__':
    exportRss() 
