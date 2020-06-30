import selenium
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

# Get initial dataset 
def get_initial_payload(url: str):
    log.debug(f'URL > {url}')
    browser.get(url)
    elements = browser.find_elements_by_tag_name('section')
    log.debug(f'Found {len(elements)} elements')

    return elements

def iterate_a(element_list: list, text_element_list: list = []) -> list:
    if element_list[-1] == element_list[-2]: 
        log.debug(f'ENDING ..... found {len(element_list)} elements')

        # Drop the last element before returning because when the else reaches 
        # the end of the content, it still add the last element to the 
        # element_list. In other words, we will add the last element to the 
        # list and then compare to previous element in the next step. This 
        # comparison then tells us whether or not thr elements are equal
        return element_list[:-1], text_element_list[:-1]
    else:
        click(element_list[-1])
        element_list.append(browser.find_elements_by_tag_name('section')[-1])
        text_element_list.append(get_element_as_text(element_list[-1]))

        return iterate_a(element_list, text_element_list)

def click(element):
    e = element.find_elements_by_tag_name('div')[-1]
    action = ActionChains(browser)
    action.move_to_element(e).click().perform()

def get_element_as_text(element):
    s = None
    try:
        s = element.get_attribute('outerHTML')
    except selenium.common.exceptions.StaleElementReferenceException as error:
        # Just log and don't take action as the text for stale elements has been
        # captured in the text_element list 
        log.error(f'IGNORE > {error.msg}')

    return s

def get_content():
    elems = get_initial_payload('https://medium.com/series/sample-3d219d98b481')
    text_elements = [get_element_as_text(e) for e in elems]
    #log.debug(text_elements)
    elems, text_elements = iterate_a(elems, text_elements)
    log.info(f'Found {len(text_elements)}, {len(elems)} elements')

    return text_elements

if __name__ == '__main__':
    get_content()