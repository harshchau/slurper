from harvester import get_series
import logging 

'''
Simulates an external library calling get.py
to test logging
'''

logging.basicConfig(level = logging.DEBUG)
logging.getLogger('get').setLevel(logging.INFO)
get_series('https://medium.com/series/py-6c6c7d22788f')