import requests
import xml.etree.ElementTree as ET 
import html2text
from sys import argv

def loadRSS(url):
    resp = requests.get(url)
    return resp

def getItems(rssURL) -> dict:
    ns = {'dc': 'http://purl.org/dc/elements/1.1/', 
            'content': 'http://purl.org/rss/1.0/modules/content/'
        }
    posts = {}
    tree = ET.fromstring(loadRSS(rssURL).text)
    for item in tree.iter('item'):
        title = item.find('title').text
        content = item.find('content:encoded', ns)
        posts[title] = html2text.html2text(content.text)
    
    return posts

def export():
    url = 'https://medium.com/feed/@'
    try:
        user_name = argv[1]
    except IndexError:
        print('Enter the medium username')
        user_name = input('> ')
    
    mkdwn = ''
    posts = getItems(url + user_name)
    for title, content in posts.items():
        mkdwn += '#' + title + '\n\n' + content
    
    print(mkdwn)

if __name__ == '__main__':
    export() 