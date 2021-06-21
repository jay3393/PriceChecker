import requests
from bs4 import BeautifulSoup
import time
import re

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}

def print_product_info(name, price, url):
    print('==================================================')
    print(f'Product >> {name}')
    print(f'Price >> {price}')
    print(f'Link >> {url}')
    print('==================================================\n')

def best_buy_check_price(URL):
    '''Checks the product name and price on Best Buy website
        returns the name and price'''
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    try:
        product = soup.find('h1', class_='heading-5 v-fw-regular').text
        price = soup.find('div', class_='priceView-hero-price priceView-customer-price').find('span').text
    except:
        print('Failed to retrieve data')
        return

    print_product_info(product, price, URL)

def walmart_check_price(URL):
    '''Checks the product name and price on Walmart website
        returns the name and price'''
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    try:
        product = soup.find('h1', class_='prod-ProductTitle prod-productTitle-buyBox font-bold').text
        price = soup.find('span', class_='price display-inline-block arrange-fit price price--stylized').find('span', class_ = 'visuallyhidden').text
    except:
        print('Failed to retrieve data')
        return

    print_product_info(product, price, URL)

def microcenter_check_price(URL):
    '''Checks the product name and price on Microcenter website
        returns the name and price'''
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    try:
        details = soup.find('div', id='details').findAll('span')
        product = details[1].text
        price = soup.find('span', id='pricing').text
    except:
        print('Failed to retrieve data\n')
        return

    print_product_info(product, price, URL)

def case_switch(arg, URL):
    '''Calls the function for the matching URL'''
    switcher = {
        'bestbuy.com': best_buy_check_price,
        'walmart.com': walmart_check_price,
        'microcenter.com': microcenter_check_price,
    }
    func = switcher.get(arg, lambda: 'Invalid URL')
    func(URL)

def find_site(URL=None):
    '''Use regex to determine the function to call based on the URL'''
    pattern = re.compile(r'\w+\.(com|net)')
    filter = pattern.search(URL)
    case_switch(str(filter.group()), URL)


if __name__ == '__main__':
    with open('products.txt', 'r') as f:
        lines = f.read().splitlines()
    while True:
        print('Updating prices...')
        start_time = time.time()

        for line in lines:
            find_site(line)

        time_taken = time.time() - start_time
        print(f'Found results ({time_taken} secs)')
        delay = .1
        time.sleep(60*delay)

    f.close()