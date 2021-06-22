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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PriceChecker:

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
    }

    console_log = ""
    tasks = 0
    completed_tasks = 0

    details = []

    def print_product_info(self, name, price, url):
        # print('==================================================')
        # print(f'Product >> {name}')
        # print(f'Price >> {price}')
        # print(f'Link >> {url}')
        # print('==================================================\n')
        self.console_log += "==================================================\n"
        self.console_log += (f'Product >> {name}\n')
        self.console_log += (f'Price >> {price}\n')
        self.console_log += (f'Link >> {url}\n')
        self.console_log += ('==================================================\n')

        # # Not a JSON, it is a dic
        # for i in range(3):
        #     product = {
        #         "name": name,
        #         "store": url,
        #         "currentPrice": price,
        #     }
        #
        #     self.details.append(product)
        #
        #     # This is a JSON
        # details_json = json.dumps(self.details)
        #
        # nameone = json.loads(details_json)
        # print(nameone[0]['name'])
        # print(nameone[0]['store'])
        # print(nameone[0]['currentPrice'])

    def best_buy_check_price(self, URL):
        '''Checks the product name and price on Best Buy website
            returns the name and price'''
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            product = soup.find('h1', class_='heading-5 v-fw-regular').text
            price = soup.find('div', class_='priceView-hero-price priceView-customer-price').find('span').text
            print(f'Success! {URL}')
            self.completed_tasks += 1
        except:
            print('Failed to retrieve data')
            return

        self.print_product_info(product, price, URL)

    def walmart_check_price(self, URL):
        '''Checks the product name and price on Walmart website
            returns the name and price'''
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            product = soup.find('h1', class_='prod-ProductTitle prod-productTitle-buyBox font-bold').text
            price = soup.find('span', class_='price display-inline-block arrange-fit price price--stylized').find('span', class_ = 'visuallyhidden').text
            print(f'Success! {URL}')
            self.completed_tasks += 1
        except:
            #self.capcha(URL)
            print(f'Failed to retrieve data for {URL}')

            return

        self.print_product_info(product, price, URL)

    def microcenter_check_price(self, URL):
        '''Checks the product name and price on Microcenter website
            returns the name and price'''
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            details = soup.find('div', id='details').findAll('span')
            product = details[1].text
            price = soup.find('span', id='pricing').text
            print(f'Success! {URL}')
            self.completed_tasks += 1
        except:
            print('Failed to retrieve data\n')
            return

        self.print_product_info(product, price, URL)

    def case_switch(self, arg, URL):
        '''Calls the function for the matching URL'''
        switcher = {
            'bestbuy.com': self.best_buy_check_price,
            'walmart.com': self.walmart_check_price,
            'microcenter.com': self.microcenter_check_price,
        }
        func = switcher.get(arg, lambda: 'Invalid URL')
        func(URL)

    def find_site(self, URL):
        '''Use regex to determine the function to call based on the URL'''
        pattern = re.compile(r'\w+\.(com|net)')
        filter = pattern.search(URL)
        self.case_switch(str(filter.group()), URL)

    def capcha(self, URL):
        '''Method for manual verification'''
        driver = webdriver.Chrome(executable_path='D:\chromedriver.exe')
        driver.get(URL)
        time.sleep(3)
        element = driver.find_element_by_class_name('recaptcha-checkbox-border')
        element.click()
        time.sleep(2)

if __name__ == '__main__':
    checker = PriceChecker()
    with open('products.txt', 'r') as f:
        lines = f.read().splitlines()
    f.close()
    checker.tasks = len(lines)
    while True:
        checker.completed_tasks = 0
        print('Updating prices...')
        start_time = time.time()

        for line in lines:
            checker.find_site(line)

        print(checker.console_log)
        checker.console_log = ""

        time_taken = time.time() - start_time
        print(f'Found results ({checker.completed_tasks}/{checker.tasks}) in {time_taken} secs')
        delay = 1
        sec_in_min = 60
        time.sleep(sec_in_min*delay)
