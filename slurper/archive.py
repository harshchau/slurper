from dataclasses import dataclass 
from dataclasses import field
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from json import JSONEncoder
import tldextract 
from functools import wraps
import time

@dataclass 
class Archive:
    publication_url: str = None
    time_requested: int = datetime.now().timestamp()
    child_data_set: [] = None

'''
Primer on how to use wraps for this decorator 
https://www.saltycrane.com/blog/2010/03/simple-python-decorator-examples/
'''
def _timer_function_run(f):
    @wraps(f)
    def timer(*args, **kwargs):
        start_time = time.time()
        print(f'Timer for archive URL: {args}')
        r = f(*args, **kwargs)
        end_time = time.time()
        print(f'Time taken: {(end_time - start_time) * 1000:.9f} ms')
        return r
    return timer

'''
Class to contain all features related to archives
'''
class ArchiveProcessor:
    tracker = dict()

    def __init__(self, archive_url):
        # This check is required only on the initial URL. This is due to the behavior of medium
        # where for an archive, a wrong url still returns the archive page for the url.
        # This check is not required for right initial urls as that check is done when 
        # local_list is created 
        if self.is_url_valid(archive_url) is False:
            raise Exception(f'Invalid archive URL: {archive_url}')
        else:
            self.tracker.update({archive_url:{'key':self.get_url_info(archive_url)['key'], 'post-urls':self.get_archive_post_urls(archive_url)}})

    @_timer_function_run
    def get_timebuckets(self, url_list): 
        u = url_list.pop()
        # If url is a date url, return. At this point, all peer date urls have been added to url_list and tracker
        if self.get_url_info(u)['is_date_url']:
            if len(url_list) == 0: # To prevent breaks when starting input is a date url only (url_list will be empty)
                return self.tracker # Done 
            else:
                return self.get_timebuckets(url_list) # Keep going 
        html_doc = requests.get(u).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        timeline_tags = soup.find_all('div', class_='timebucket')
        local_list = [t.a['href'] for t in timeline_tags if t.a]
#        print(f'LOCAL_LIST: {len(local_list)} URL_LIST: {len(url_list)} TRACKER: {len(self.tracker)} URL: {u}')
        url_list.extend(local_list)
        self.tracker.update({u:{'key':self.get_url_info(u)['key'],'post-urls':self.get_archive_post_urls(u)} for u in local_list})

        if len(url_list) == 0:
            return self.tracker # Done 
        else:
            return self.get_timebuckets(list(sorted(set(url_list)))) # Keep going 

    def get_url_info(self, url: str):
        url_info = {'is_date_url': False}
        extract = tldextract.extract(url)
        suffix = extract.suffix
        rest = url[url.index(suffix) + len(suffix):]
        split_rest = rest.split('/')
        split_rest = [i for i in split_rest if i != '']
        if len(split_rest) == 4: url_info['is_date_url'] = True

        url_info['key'] = '#'.join(split_rest[1:])

        return url_info
    # Just called during __init__
    def is_url_valid(self, url):
        ret = False 
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        timeline_tags = soup.find_all('div', class_='timebucket')
        local_list = [t.a['href'] for t in timeline_tags if t.a]
        try:
            key_list = [self.get_url_info(u)['key'] for u in local_list]
            input_url_key = self.get_url_info(url)['key']
            if len([k for k in key_list if input_url_key in k]) > 0: ret = True
        except ValueError as err:
            print(err)

        return ret

    '''
        Given a URL to a publication archive (yearly, monthly, daily), get all post URL's from the archives
    '''
    def get_archive_post_urls(self, archive_url: str) -> list:
        ret = []
        html_doc = requests.get(archive_url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        sections = soup.find_all('section')
        for s in sections:
            a = s.find_parent('a')
            ret.append(a['href'])

        return ret

class ArchiveEncoder(JSONEncoder):
    def default(self, o):
        ret = o.__dict__
        return ret 

if __name__ == '__main__':
    archive_url = 'https://marker.medium.com/archive/2020/05/01'
    ap = ArchiveProcessor(archive_url)
    ap.timebuckets = ap.get_timebuckets([archive_url])
    print(json.dumps(ap.timebuckets, cls=ArchiveEncoder, indent=2))