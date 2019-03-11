# Jake Gluck - Capital News Service

# jagluck.github.io

# This is an automated web scraper that gathers all conversations between any number of twitter accounts
# To use fill download selenium and fill in its location, then fill in your accounts

import sys

#pip.main(['install','selenium'])
#pip.main(['install','bs4'])
#pip.main(['install','lxml'])

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from random import *
import json
# import requests

#Set up headless browser
#chrome_options = Options()
#chrome_options.add_argument("--headless")

#Fill in path to chromedrive.exe here
chromedriver = 'chromedriver_win.exe'

#to view browser working remove chrome_options
driver = webdriver.Chrome(chromedriver)


pages_visited = 0
link_stack = []
main_link = "https://www.reddit.com/"

#count number of pages visited
def countPage():
    global pages_visited
    pages_visited = pages_visited + 1

#scroll mentions page down
def scroll_down():
     #scroll to bottom of page
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    
    max = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
    
        driver.maximize_window()

        time.sleep(.5)
        max = max + 1
        if (max == 4):
            break

# def validateLink(url):
#     resp = False
#     try:
#         request = requests.get(url)
#         if request.status_code == 200:
#             resp = True

#     except:
#         resp = False

#     return resp

#load mentions page
def load_page(url):
    countPage()
    driver.get(url) 
    time.sleep(.2)
    scroll_down()
    #load html

    global link_stack
    soup = BeautifulSoup(driver.page_source, "lxml")
    links = soup.find_all("a", href=True)
    if (len(links) > 10):
        for i in range(1,10):
            el = randint(0,(len(links)-1))
            href = links[el]["href"]
        
            if (href.startswith("/r/") or href.startswith("/search") or href.startswith("/user/")):
                link_stack.append("https://reddit.com" + href)   

    if (len(link_stack) > 200):
        link_stack = link_stack[100:]     

    if (len(link_stack) == 0 or pages_visited%100 == 0):
        new_url = main_link
    else:          
        new_url = link_stack.pop()
    print("-------")
    print(new_url)
    load_page(new_url)   

#load specific tweet page
def load_page_tweet(url):
    countPage()
    driver.get(url) 
    time.sleep(1)

    scroll_down()
        

def check_exists_by_id(id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True


#start bot
def run_bot():
    load_page(main_link) 
    
    #load html
    soup = BeautifulSoup(driver.page_source, "lxml")
    stream = soup.find("ol", {"class": "stream-items"})


run_bot()


