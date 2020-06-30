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

def iterate_a(element_list: list) -> list:
    if element_list[-1] == element_list[-2]: 
        log.debug(f'ENDING ..... found {len(element_list)} elements')

        return element_list
    else:
        click(element_list[-1])
        element_list.append(browser.find_elements_by_tag_name('section')[-1])
        
        return iterate_a(element_list)

def click(element):
    e = element.find_elements_by_tag_name('div')[-1]
    action = ActionChains(browser)
    action.move_to_element(e).click().perform()

def get_element_as_text(element):
    return element.get_attribute('outerHTML')


if __name__ == '__main__':
    elems = get_initial_payload('https://medium.com/series/sample-3d219d98b481')
    text_elements = [get_element_as_text(e) for e in elems]
    elems_2 = iterate_a(elems)
    text_elements_2 = [get_element_as_text(e) for e in elems_2]
    text_elements.extend(text_elements_2)
    for c,e in enumerate(text_elements):
        try:
            log.debug(f'{c} > {get_element_as_text(e)}')
        except Exception as error:
            log.error(f'{c} > {error}')
    #    print(get_element_as_text(e))