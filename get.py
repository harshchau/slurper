import requests
import xml.etree.ElementTree as ET 
import html2text
from sys import argv
import logging 
from bs4 import BeautifulSoup

# TO BE DEPRECATED - RSS sucks for Medium
def load_rss(url):
    resp = requests.get(url)
    return resp

# TO BE DEPRECATED - RSS sucks for medium
def get_rss_items(rssURL) -> dict:
    ns = {'dc': 'http://purl.org/dc/elements/1.1/', 
            'content': 'http://purl.org/rss/1.0/modules/content/'
        }
    posts = {}
    tree = ET.fromstring(load_rss(rssURL).text)
    for item in tree.iter('item'):
        try:
            title = item.find('title').text
            content = item.find('content:encoded', ns)
            posts[title] = html2text.html2text(content.text)
        except Exception as e:
            logging.error(f'Error in title: {title} | Error message: {e}', exc_info = True)
    
    return posts

# TO BE DEPRECATED - RSS sucks for medium
def export_rss():
    url = 'https://medium.com/feed/@'
    try:
        user_name = argv[1]
    except IndexError:
        user_name = input('Enter a username > ')
    
    mkdwn = ''
    posts = get_rss_items(url + user_name)
    for title, content in posts.items():
        mkdwn += '#' + title + '\n\n' + content
    
    print(mkdwn)

def get_series(url:str) -> None:
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    series_header = soup.find_all('h1')[0].get_text()
    print(series_header)
    main_html_node = soup.find_all(attrs={'id'})
    #print(soup.prettify(main_html_node))
    print((main_html_node))

if __name__ == '__main__':
    #export_rss() 
    get_series('https://medium.com/series/py-6c6c7d22788f')
