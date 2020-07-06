from slurper import harvester
import logging

'''
Simulates an external library calling harvester.py
'''

logging.basicConfig(level = logging.DEBUG)
logging.getLogger('get').setLevel(logging.INFO)
harvester.get_series('https://medium.com/series/py-6c6c7d22788f', True, False, False)