import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
import validators
import json

browser = webdriver.Chrome()
url = 'https://scholar.google.com/'
browser.get(url=url)

html = browser.execute_script("return document.documentElement.outerHTML")
html[:3000]

q_element = browser.find_element(By.CSS_SELECTOR, 'input[name=q]')
q_element.clear()
q_element.send_keys('Thailand Paper')

q_element.send_keys(u'\ue007')
all_element = browser.find_elements(By.CSS_SELECTOR, '.gs_ri')

websites_dict = {}
i = 0
for element in all_element:
    website_dict = {}
    a_tag = element.find_element(By.TAG_NAME, 'a')
    website_dict["title"] = a_tag.text
    # print(a_tag.text)
    website_dict["related_link"] = a_tag.get_attribute('href')
    a_tag.click()
    # if(browser.current_url == "https://scholar.google.com/"):
    #     q_element = browser.find_element(By.CSS_SELECTOR, 'input[name=q]')
    #     q_element.clear()
    #     q_element.send_keys('Thailand Paper')
    #     q_element.send_keys(u'\ue007')
    # else:
    name = element.find_element(By.CSS_SELECTOR, '.gs_a')
    website_dict["author"] = name.text

    browser.back()
    time.sleep(2)
    # print(a_tag.get_attribute('href'))
    websites_dict[i] = website_dict
    i+=1

json_string = json.dumps(websites_dict, indent=4)
print(json_string)
   

all_links = browser.find_elements(By.CSS_SELECTOR, '.gs_ri a')

# Iterate through the links by index to avoid stale references
for i in range(len(all_links)):
    # Re-locate the links after navigation to ensure they are fresh
    all_links = browser.find_elements(By.CSS_SELECTOR, '.gs_ri a')

    # Click the current link
    all_links[i].click()

    # Perform actions on the new page
    print("Current URL:", browser.current_url)

    # Navigate back to the previous page
    browser.back()

    if(browser.current_url == "https://scholar.google.com/"):
        q_element = browser.find_element(By.CSS_SELECTOR, 'input[name=q]')
        q_element.clear()
        q_element.send_keys('Thailand Paper')
        q_element.send_keys(u'\ue007')

    # Optional: Wait for the page to reload fully
    time.sleep(5)