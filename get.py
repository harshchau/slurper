import requests
import xml.etree.ElementTree as ET 
import html2text

def loadRSS(url):
    resp = requests.get(url)
    return resp

def getItems(rssURL):
    ns = {'dc': 'http://purl.org/dc/elements/1.1/', 
            'content': 'http://purl.org/rss/1.0/modules/content/'
        }
    tree = ET.fromstring(loadRSS(rssURL).text)
    for item in tree.iter('item'):
        title = item.find('title').text
        if title != 'Sample': return
        else:
            content = item.find('content:encoded', ns)
            return html2text.html2text(content.text)


mkdwn = getItems('https://medium.com/feed/@harshchau')
print(mkdwn)