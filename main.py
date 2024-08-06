# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 22:32:03 2024

@author: carlo
"""
from flask import Flask
from selenium import webdriver
import chromedriver_binary # Adds chromedriver binary to path

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

app = Flask(__name__)

def request_url(driver, 
                url : str):
    e, status = None, '' # error
    # request url
    try:
        driver.get(url)
        driver.implicitly_wait(30)
        status += f'{url} successfully requested.'
    # error in requesting url
    except Exception as e:
        status += f'{e.msg}'
    
    # request url success
    # check if reactivate button is present
    try:
        sleep_btn = driver.find_element(By.XPATH, 
                                        '//button[@type="button"]')
        status += f'\n{url} is asleep.'
    # app is active
    except:
        status += '\nApp is active.'
        
    # app asleep
    if (sleep_btn is not None) and (sleep_btn.text == 'Yes, get this app back up!'):
        # reawaken app
        sleep_btn.click()
        # wait until active app element is present
        wait = WebDriverWait(driver, timeout = 180)
        active_app_elem = f"{url.split('https:')[-1]}~/+/"
        # wait until app reawakens
        try:
            wait.until(EC.presence_of_element_located((By.XPATH,
                                                  f'//iframe[@src="{active_app_elem}"]')))
            status += f'\n{url} reawakened from sleep status.'
        # error in activating app
        except Exception as e:
            status += f'\n{e.msg}'
            
    if e is None:
        status = '\nSuccess'
    
    return {'url' : driver.current_url,
            'status' : status}

@app.route('/')
def wake_urls(*args):
    urls = ['https://mechanigo-customer-retention-zr1lfy99foh.streamlit.app/',
            'https://gulong-superapp.streamlit.app/']
    
    results = {}
    # create chromedriver instance
    driver = Chrome(options = options)
    
    for url in urls:
        print (f'Requesting {url}.')
        results[url] = request_url(driver, url)
    
    driver.close()
    
    return results