from dataclasses import dataclass 
from dataclasses import field
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from json import JSONEncoder
import tldextract 

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
    tracker_list = dict()

    def __init__(self, archive_url):
        # get html string
        html_doc = requests.get(archive_url).text
        # make some soup
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        self.tracker_list.update({archive_url:self.get_url_info(archive_url)['key']})

    def get_timebuckets(self, url_list): 
#        print(url_list)
        u = url_list.pop()
        # If url is a date url, return. At this point, all peer date urls have been added to url_list and tracker_list
        if self.get_url_info(u)['is_date_url']:
            if len(url_list) == 0: # To prevent breaks when starting input is a date url only (url_list will be empty)
                return self.tracker_list
            else:
                return self.get_timebuckets(url_list)
        html_doc = requests.get(u).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        timeline_tags = soup.find_all('div', class_='timebucket')
        local_list = [t.a['href'] for t in timeline_tags if t.a]
#        print(f'LOCAL_LIST: {len(local_list)} URL_LIST: {len(url_list)} TRACKER_LIST: {len(self.tracker_list)} URL: {u}')
        url_list.extend(local_list)
        self.tracker_list.update({i:self.get_url_info(i)['key'] for i in local_list})

        if len(url_list) == 0:
#            for k,v in self.tracker_list.items():
#                print(k,v)
            return self.tracker_list
        else:
            return self.get_timebuckets(list(sorted(set(url_list))))

    def get_url_info(self, url: str):
        url_info = {'is_date_url': False}
        extract = tldextract.extract(url)
        suffix = extract.suffix
        rest = url[url.index(suffix) + len(suffix):]
        split_rest = rest.split('/')
        split_rest = [i for i in split_rest if i != '']
#        print(split_rest) # For date urls ['', 'archive', '2019', '12', '30']
        # The second condition handles the issue with a trailing slash. We get non date urls identified as dates
        if len(split_rest) == 4: url_info['is_date_url'] = True

        url_info['key'] = '#'.join(rest.split('/')[2:])

        return url_info

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
    archive_url = 'https://marker.medium.com/archive/2019/11/10'
    ap = ArchiveProcessor(archive_url)
    ap.timebuckets = ap.get_timebuckets([archive_url])
    print(json.dumps(ap.timebuckets, cls=ArchiveEncoder, indent=2))

#    a = Archive(publication, datetime.now().timestamp(), {'ALL': ap.get_archive_post_urls()})
#    print(json.dumps(a, cls = ArchiveEncoder, indent=2))