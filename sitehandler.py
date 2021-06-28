'''
Pre-processing data retrieval tool
Read textfile of products from supported sites and determine proper framework function to use for each corresponding product.
Sends requests for each product and retrieve data of product name, price, and URL.
Prints to console log and calls the save function to logdata.py

Currently supports BestBuy, Walmart, Microcenter (To add more, define the function for that website)
'''

import requests
from bs4 import BeautifulSoup
import re
import productData

class SiteHandler():
    '''
    Input: URL
    Output: Data of product (name, store, price, URL)
    '''

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
    }

    def __init__(self, tasks):
        self.completed_tasks = 0
        self.total_tasks = tasks

    def get_request(self, URL):
        try:
            r = requests.get(URL, headers=self.headers, timeout=(1,2))
            soup = BeautifulSoup(r.content, 'lxml')
            return soup
        except TimeoutError:
            print(f"Timed Out: {URL}")
            return soup
        except:
            print(f'Failed to retrieve data for {URL}')
            return soup

    def best_buy_check_price(self, URL):
        '''
        Checks the product name and price on Best Buy website
        returns the name and price
        '''
        store = 'BestBuy'
        soup = self.get_request(URL)

        try:
            product = soup.find('h1', class_='heading-5 v-fw-regular').text
            price = soup.find('div', class_='priceView-hero-price priceView-customer-price').find('span').text
            print(f'Success! {URL}')
            self.completed_tasks += 1
        except:
            print(f'Failed to retrieve data for {URL}')
            return None

        return productData.Product(product, price, URL, store)


    def walmart_check_price(self, URL):
        '''
        Checks the product name and price on Walmart website
        returns the name and price
        '''
        store = 'Walmart'
        soup = self.get_request(URL)
        # r = requests.get(URL, headers=self.headers)
        # soup = BeautifulSoup(r.content, 'lxml')

        try:
            product = soup.find('h1', class_='prod-ProductTitle prod-productTitle-buyBox font-bold').text
            price = soup.find('span', class_='price display-inline-block arrange-fit price price--stylized').find('span', class_ = 'visuallyhidden').text
            print(f'Success! {URL}')
            self.completed_tasks += 1
        except:
            print(f'Failed to retrieve data for {URL}')
            return None

        return productData.Product(product, price, URL, store)


    def microcenter_check_price(self, URL):
        '''
        Checks the product name and price on Microcenter website
        returns the name and price
        '''
        store = 'Micro Center'
        soup = self.get_request(URL)
        # r = requests.get(URL, headers=self.headers)
        # soup = BeautifulSoup(r.content, 'lxml')

        try:
            details = soup.find('div', id='details').findAll('span')
            product = details[1].text
            price = soup.find('span', id='pricing').text
            print(f'Success! {URL}')
            self.completed_tasks += 1
        except:
            print(f'Failed to retrieve data for {URL}')
            return None

        return productData.Product(product, price, URL, store)

    #   ###############################################
    #   FIX CASE SWITCH TO HANDLE EXCEPTIONS AND ERRORS
    #   ###############################################
    def case_switch(self, arg, URL):
        '''
        Calls the function for the matching URL
        Add switcher element when adding new site
        '''
        switcher = {
            'bestbuy.com': self.best_buy_check_price,
            'walmart.com': self.walmart_check_price,
            'microcenter.com': self.microcenter_check_price,
        }
        func = switcher.get(arg, lambda: 'Website not supported')
        if func != 'Website not supported':
            return func(URL)

    def find_site(self, URL):
        '''
        Use regex to determine the function to call based on the URL
        '''
        pattern = re.compile(r'\w+\.(com|net)')
        filter = pattern.search(URL)
        return self.case_switch(str(filter.group()), URL)