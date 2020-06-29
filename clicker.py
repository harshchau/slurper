from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

'''
Use a headless browser to navigate a series or post and get the entire dataset.
'''

# Set up headless browser
# Get initial dataset
# Click on last element to get the next 
# Add the newly received element to the initial dataset 
# Repeat 


# Set up headless browser 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--headless") 
browser = webdriver.Chrome(chrome_options=chrome_options)

# Get initial dataset 
browser.get('https://medium.com/series/sample-3d219d98b481')
elements = browser.find_elements_by_tag_name('section')

first_element = elements[0]
html = first_element.get_attribute('outerHTML')
print('FIRST >>>>> ', html)

last_element = elements[-1]
html = last_element.get_attribute('outerHTML')
print('Last >>>>> ', html)

print('CLICK on > ', first_element.get_attribute('outerHTML'))
a = first_element.click()
elements = browser.find_elements_by_tag_name('section')
last_element = elements[-1]
html = last_element.get_attribute('outerHTML')
print('Latest >>>>> ', html)
#elements.append(last_element)

#print('LAST ELEMENT FROM ELEMENTS >>>>> ', elements[-1].get_attribute('outerHTML'))

e = last_element.find_element_by_id('be83')
action = ActionChains(browser)
action.move_to_element(e).click().perform()

elements = browser.find_elements_by_tag_name('section')
a = elements[-1]

print(')))))))))))) > ', a.get_attribute('outerHTML'))