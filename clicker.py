from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--headless") 

browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://medium.com/series/sample-3d219d98b481')
elements = browser.find_elements_by_tag_name('section')

first_element = elements[0]
html = first_element.get_attribute('outerHTML')
print('FIRST >>>>> ', html)

last_element = elements[-1]
html = last_element.get_attribute('outerHTML')
print('Last >>>>> ', html)

a = first_element.click()
elements = browser.find_elements_by_tag_name('section')
last_element = elements[-1]
html = last_element.get_attribute('outerHTML')
print('Last >>>>> ', html)