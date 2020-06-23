import requests
import xml.etree.ElementTree as ET 
import html2text

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

def export(url: str):
    mkdwn = ''
    posts = getItems(url)
    for title, content in posts.items():
        mkdwn += '#' + title + '\n\n' + content

    return mkdwn 


mkdwn = export('https://medium.com/feed/@harshchau')
print(mkdwn)