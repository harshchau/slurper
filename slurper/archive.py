from dataclasses import dataclass 
from dataclasses import field
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from json import JSONEncoder

@dataclass 
class Archive:
    publication_url: str = None
    time_requested: int = datetime.now().timestamp()
    child_data_set: [] = None

'''
Class to contain all features related to archives
'''
class ArchiveProcessor:
    soup = None 
    timebuckets = {}
    tracker_set = set()

    def __init__(self, archive_url):
        # get html string
        html_doc = requests.get(archive_url).text
        # make some soup
        self.soup = BeautifulSoup(html_doc, 'html.parser')

    def get_timebuckets(self, url_list): 
#        print('RECEIVED', len(url_list), url_list)
        # get html string
        u = url_list.pop()
        html_doc = requests.get(u).text
        # make some soup
        soup = BeautifulSoup(html_doc, 'html.parser')
        timeline_tags = soup.find_all('div', class_='timebucket')
#        self.timebuckets.update({t.a.string:t.a['href'] for t in timeline_tags})
#        print(self.timebuckets)
#        if len(timeline_tags) > 0:
        local_set = {t.a['href'] for t in timeline_tags if t.a}
#            print('TYPE', type(local_set), type(url_list))
#        print('######################')
#        print('LOCAL_SET', len(local_set), local_set)
#        print( )
#        print('URL_LIST', len(url_list), url_list)
#        print(local_set == url_list)
        print(f'LOCAL_SET: {len(local_set)} URL_LIST: {len(url_list)} TRACKER_SET: {len(self.tracker_set)} URL: {u}')
#        print('<<<<<<<<<<<<<<<<<<<<<<')
        self.tracker_set.update(local_set)
        url_list.update(local_set)

        return self.get_timebuckets(sorted(url_list))

    '''
        Given a URL to a publication archive (yearly, monthly, daily), get all post URL's from the archives
    '''
    def get_archive_post_urls(self) -> list:
        ret = []
        sections = self.soup.find_all('section')
        for s in sections:
            a = s.find_parent('a')
            ret.append(a['href'])

        return ret

class ArchiveEncoder(JSONEncoder):
    def default(self, o):
        ret = o.__dict__
        return ret 

if __name__ == '__main__':
    archive_url = 'https://marker.medium.com/archive/2019'
    ap = ArchiveProcessor(archive_url)
    ap.timebuckets = ap.get_timebuckets({archive_url,})
#    print(ap.timebuckets)

#    a = Archive(publication, datetime.now().timestamp(), {'ALL': ap.get_archive_post_urls()})
#    print(json.dumps(a, cls = ArchiveEncoder, indent=2))