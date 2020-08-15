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
from concurrent import futures 
from concurrent.futures import ThreadPoolExecutor

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
        if(type(args[1])) == list:
            urls = args[1].copy()
        else:
            urls = args[1]
        r = f(*args, **kwargs)
        end_time = time.time()
        print(f'Time taken > Method: {f.__name__} Url: {urls} {(end_time - start_time) * 1000:.9f} ms')
        return r
    return timer

'''
Class to contain all features related to archives
'''
class ArchiveProcessor:
    tracker = dict()
    soup = None
    ex = None

    def __init__(self, archive_url):
        html_doc = requests.get(archive_url).text
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        # This check is required only on the initial URL. This is due to the behavior of medium
        # where for an archive, a wrong url still returns the archive page for the url.
        # This check is not required for right initial urls as that check is done when 
        # local_list is created 
        if archive_url[-1] == '/': # Trailing slash is a directory and was being caught as an error due to a 301 at the end
            archive_url = archive_url[:-1]
#            print('ARCHIVE url', type(archive_url), archive_url)
        if self.is_url_valid(archive_url) is False:
            raise Exception(f'Invalid archive URL: {archive_url}')
        else:
            self.tracker.update({archive_url:{'key':self.get_url_info(archive_url)['key'], 'post-urls':self.get_archive_post_urls(archive_url)}})
        self.ex = futures.ThreadPoolExecutor(max_workers=20) # 20 workers seems to be ideal


#    @_timer_function_run
    def get_timebuckets(self, url_list): 
    #    print(url_list)
        u = url_list.pop()

        # If url is a date url, return. At this point, all peer date urls have been added to url_list and tracker
        if self.get_url_info(u)['is_date_url']:
            if len(url_list) == 0: # To prevent breaks when starting input is a date url only (url_list will be empty)
                print('GETTING 1')
                return self.tracker # Done 
            else:
                print('GETTING 2')
                return self.get_timebuckets(url_list) # Keep going 

#        print(f'LOCAL_LIST: {len(local_list)} URL_LIST: {len(url_list)} TRACKER: {len(self.tracker)} URL: {u}')

        local_list = self._get_child_calendar_urls(u)

        ################
        # Concurrent calls to get archive post urls for local list
##        archive_post_urls_for_local_list = self.ex.map(self.get_archive_post_urls, local_list)
##        real_results = list(archive_post_urls_for_local_list)
        # Store all archive post urls for each url in the local list in a dictionary
##        dict_of_archive_post_urls_for_local_list = {u:real_results[local_list.index(u)] for u in local_list}
        ################
        

        url_list.extend(local_list)
        self.tracker.update({u:{'key':self.get_url_info(u)['key'],'post-urls':self.get_archive_post_urls(u)} for u in local_list})

        if len(url_list) == 0:
            return self.tracker # Done 
        else:
            return self.get_timebuckets(list(sorted(set(url_list)))) # Keep going 

    def _get_child_calendar_urls(self, url):
        #html_doc = requests.get(url).text
        #soup = BeautifulSoup(html_doc, 'html.parser')
        timeline_tags = self.soup.find_all('div', class_='timebucket')
        local_list = [t.a['href'] for t in timeline_tags if t.a]
#        print('>>>>>', local_list)

        return local_list

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
    
    # Just called during __init__ but is called multiple times from the Lambda
    def is_url_valid(self, url):
        ret = False 
        response = requests.get(url)
        last_resp = response.history[-1]
        print('RESPONSE', last_resp.status_code, last_resp.url, response.history)
        # Just this is not enough. I can send in a date like 2019/09/99 and that is valid
        # but 2019/09/100 is invalid
        if last_resp.status_code == 301: # 2019/09/100
            ret = False 
        elif last_resp.status_code == 302 and len(response.history) > 2: # 2019/09/50
            ret = False 
        else:
            ret = True
#        html_doc = response.text
#        soup = BeautifulSoup(html_doc, 'html.parser')
#        timeline_tags = soup.find_all('div', class_='timebucket')
#        local_list = [t.a['href'] for t in timeline_tags if t.a]
#        try:
#            key_list = [self.get_url_info(u)['key'] for u in local_list]
#            input_url_key = self.get_url_info(url)['key']
#            print('#####', type(input_url_key), input_url_key)
#            print('#####', type(key_list), type(key_list[0]), key_list)
            # Using in becase we want to test for whether 2020/08 (month) also exists in 
            # 2020/08/03 (day)
#            if len([k for k in key_list if input_url_key in k]) > 0: ret = True 
#        except ValueError as err:
#            print(err)

        return ret

    '''
        Given a URL to a publication archive (yearly, monthly, daily), get all post URL's from the archives
    '''
#    @_timer_function_run
    def get_archive_post_urls(self, archive_url: str, soup = None) -> list:
        ret = []
        #response = requests.get(archive_url)
        #html_doc = response.text
        #soup = BeautifulSoup(html_doc, 'html.parser')
        sections = self.soup.find_all('section')
        for s in sections:
            a = s.find_parent('a')
            ret.append(a['href'])

#        print(f'get_archive_post_urls for {archive_url}')
        return ret

class ArchiveEncoder(JSONEncoder):
    def default(self, o):
        ret = o.__dict__
        return ret 

if __name__ == '__main__':
    archive_url = 'https://marker.medium.com/archive/2020/08/03'
    ap = ArchiveProcessor(archive_url)
    ap.timebuckets = ap.get_timebuckets([archive_url])
    print(json.dumps(ap.timebuckets, cls=ArchiveEncoder, indent=2))