import requests
from bs4 import BeautifulSoup
import time
import re

class PriceChecker:

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
    }

    console_log = ""

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

    def best_buy_check_price(self, URL):
        '''Checks the product name and price on Best Buy website
            returns the name and price'''
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            product = soup.find('h1', class_='heading-5 v-fw-regular').text
            price = soup.find('div', class_='priceView-hero-price priceView-customer-price').find('span').text
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
        except:
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
        print(URL)
        filter = pattern.search(URL)
        self.case_switch(str(filter.group()), URL)


if __name__ == '__main__':
    checker = PriceChecker()
    with open('products.txt', 'r') as f:
        lines = f.read().splitlines()
    while True:
        #console_log = ""
        print('Updating prices...')
        start_time = time.time()

        for line in lines:
            checker.find_site(line)

        print(checker.console_log)
        checker.console_log = ""

        time_taken = time.time() - start_time
        print(f'Found results ({time_taken} secs)')
        delay = .1
        time.sleep(60*delay)

    f.close()