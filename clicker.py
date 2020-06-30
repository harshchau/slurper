from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import logging

'''
Use a headless browser to navigate a series or post and get the entire dataset
Steps:
    # Set up headless browser
    # Get initial dataset
    # Click on last element to get the next 
    # Add the newly received element to the initial dataset 
    # Repeat 
'''

# Logging config 
logging.basicConfig(level = logging.ERROR)
log = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)

# Set up headless browser 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--headless") 
browser = webdriver.Chrome(chrome_options=chrome_options)

elements = []

# Get initial dataset 
def get_initial_payload():
    browser.get('https://medium.com/series/sample-3d219d98b481')
    elements = browser.find_elements_by_tag_name('section')

    return elements

def iterate(elements: list, last_len = len(elements)):
    if last_len == len(elements): 
        return elements
    else:
        curr_len = len(elements)
        click(get_last_element(elements))
        e = get_last_element(elements)
        print_element(e)
        iterate(elements, curr_len)

    #e = get_last_element(elements)
    #click(e)
    #e = get_last_element(elements)
    #print_element(e)

def click(element):
    e = element.find_elements_by_tag_name('div')[-1]
    action = ActionChains(browser)
    action.move_to_element(e).click().perform()

def get_last_element(elements):
    return browser.find_elements_by_tag_name('section')[-1]

def print_element(element: list):
    print(element.get_attribute('outerHTML'))


if __name__ == '__main__':
    elements = iterate(get_initial_payload())