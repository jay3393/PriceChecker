import requests
from bs4 import BeautifulSoup
import time
import re

url1 = 'https://www.bestbuy.com/site/razer-kraken-ultimate-wired-thx-spatial-audio-gaming-headset-for-pc-with-rgb-lighting-classic-black/6391902.p?skuId=6391902'

url2= 'https://www.walmart.com/ip/Razer-Kraken-X-Multi-Platform-Wired-Gaming-Headset-Black/323390578'

url3 = 'https://www.microcenter.com/product/615492/razer-kraken-x-wired-gaming-headset'

url4 = 'https://www.microcenter.com/product/627723/turtle-beach-stealth-700-gen-2-premium-wireless-gaming-headset'

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

    product = soup.find('h1', class_ = 'heading-5 v-fw-regular').text
    price = soup.find('div', class_ = 'priceView-hero-price priceView-customer-price').find('span').text
    # print(f'\nProduct: {product}')
    # print(f'Price: {price}')
    # print(f'Link: {URL}')
    print_product_info(product, price, URL)

def walmart_check_price(URL):
    '''Checks the product name and price on Walmart website
        returns the name and price'''
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    product = soup.find('h1', class_='prod-ProductTitle prod-productTitle-buyBox font-bold').text
    price = soup.find('span', class_='price display-inline-block arrange-fit price price--stylized').find('span', class_ = 'visuallyhidden').text
    print_product_info(product, price, URL)

def microcenter_check_price(URL):
    '''Checks the product name and price on Microcenter website
        returns the name and price'''
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    details = soup.find('div', id='details').findAll('span')
    product = details[1].text
    price = soup.find('span', id='pricing').text
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
    # text =  '''
    # https://www.bestbuy.com/site/razer-kraken-ultimate-wired-thx-spatial-audio-gaming-headset-for-pc-with-rgb-lighting-classic-black/6391902.p?skuId=6391902
    # https://www.walmart.com/ip/Razer-Kraken-X-Multi-Platform-Wired-Gaming-Headset-Black/323390578
    # https://www.microcenter.com/product/615492/razer-kraken-x-wired-gaming-headset
    # https://www.microcenter.com/product/627723/turtle-beach-stealth-700-gen-2-premium-wireless-gaming-headset
    # https://www2.hm.com/en_us/productpage.0685816099.html
    # https://www.target.com/c/patio-furniture-garden/all-deals/-/N-5xtorZakkos?type=products
    # https://www.aliexpress.com/item/1005002642578572.html?spm=a2g0o.productlist.0.0.35b47183j62gRT&aem_p4p_detail=202106201502137698753256523000029143816
    # https://www.alibaba.com/product-detail/1-Pc-Body-Fat-Tester-Analyzer_1600128381046.html?spm=a27aq.22883793.4119238120.13.2709bda5UKlcmS&ecology_token=default
    # '''
    pattern = re.compile(r'\w+\.(com|net)')
    filter = pattern.search(URL)
    # for match in filter:
    #     print(match)
    #print(filter.group())
    case_switch(str(filter.group()), URL)


if __name__ == '__main__':
    while True:
        print('Updating prices...')
        find_site(url1)
        find_site(url2)
        find_site(url3)
        find_site(url4)
        print('Found results')
        delay = .1
        time.sleep(60*delay)