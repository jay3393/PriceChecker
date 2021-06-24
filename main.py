'''
Pre-processing data retrieval tool
Read textfile of products from supported sites and determine proper framework function to use for each corresponding product.
Sends requests for each product and retrieve data of product name, price, and URL.
Prints to console log and calls the save function to logdata.py

Currently supports BestBuy, Walmart, Microcenter,
'''

import requests
from bs4 import BeautifulSoup
import time
import re
import json
import logdata
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sitehandler
import display

class PriceChecker:

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
    }

    console_log = ""
    tasks = 0
    completed_tasks = 0

    data = {}

'''
if __name__ == '__main__':
    checker = PriceChecker() # Instantiate the PriceChecker class
    with open('products.txt', 'r') as f: # Only need to read the file once to get all the websites
        lines = f.read().splitlines()
    f.close()
    checker.tasks = len(lines)
    while True:
        checker.completed_tasks = 0
        print('Checking prices...')
        start_time = time.time()

        for line in lines:
            checker.find_site(line)

        checker.print_console_log()
        details_json = checker.data
        checker.data = {} # resets data buffer

        time_taken = time.time() - start_time
        print(f'Found results ({checker.completed_tasks}/{checker.tasks}) in {time_taken} secs')
        updateLog = logdata.UpdateLog(details_json)
        updateLog.update()

        delay = .1
        sec_in_min = 60
        time.sleep(sec_in_min*delay)
'''

if __name__ == '__main__':
    with open('products.txt', 'r') as f: # Only need to read the file once to get all the websites
        lines = f.read().splitlines()
    f.close()
    logger = logdata.UpdateLog(None)

    print('Running price checker...')

    while True:
        sites = sitehandler.SiteHandler(len(lines))
        print('Updating prices...')
        start_time = time.time()
        for line in lines:
            data = sites.find_site(line)
        sites.displayer.print_console_log()
        #sites.displayer.packer.__print__()
        logger.data = sites.displayer.packer.data
        logger.update()
        print(f'Time took: {time.time() - start_time}')

        delay = .1
        time.sleep(60*delay)