import requests
from bs4 import BeautifulSoup
import time
import re

# URL = 'https://www.bestbuy.com/site/razer-kraken-ultimate-wired-thx-spatial-audio-gaming-headset-for-pc-with-rgb-lighting-classic-black/6391902.p?skuId=6391902'

#URL = 'https://www.walmart.com/ip/Razer-Kraken-X-Multi-Platform-Wired-Gaming-Headset-Black/323390578'

#URL = 'https://www.microcenter.com/product/615492/razer-kraken-x-wired-gaming-headset'

URL = 'https://www.microcenter.com/product/627723/turtle-beach-stealth-700-gen-2-premium-wireless-gaming-headset'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}

def best_buy_check_price():
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    product = soup.find('h1', class_ = 'heading-5 v-fw-regular').text
    price = soup.find('div', class_ = 'priceView-hero-price priceView-customer-price').find('span').text
    print(product)
    print(price)

def walmart_check_price():
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    product = soup.find('h1', class_='prod-ProductTitle prod-productTitle-buyBox font-bold').text
    price = soup.find('span', class_='price display-inline-block arrange-fit price price--stylized').find('span', class_ = 'visuallyhidden').text
    print(product)
    print(price)

def microcenter_check_price():
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    details = soup.find('div', id='details').findAll('span')
    product = details[1].text
    price = soup.find('span', id='pricing').text
    print(product)
    print(price)

def find_site(URL=None):
    text =  '''
    https://www.bestbuy.com/site/razer-kraken-ultimate-wired-thx-spatial-audio-gaming-headset-for-pc-with-rgb-lighting-classic-black/6391902.p?skuId=6391902
    https://www.walmart.com/ip/Razer-Kraken-X-Multi-Platform-Wired-Gaming-Headset-Black/323390578
    https://www.microcenter.com/product/615492/razer-kraken-x-wired-gaming-headset
    https://www.microcenter.com/product/627723/turtle-beach-stealth-700-gen-2-premium-wireless-gaming-headset
    https://www2.hm.com/en_us/productpage.0685816099.html
    https://www.target.com/c/patio-furniture-garden/all-deals/-/N-5xtorZakkos?type=products
    https://www.aliexpress.com/item/1005002642578572.html?spm=a2g0o.productlist.0.0.35b47183j62gRT&aem_p4p_detail=202106201502137698753256523000029143816
    https://www.alibaba.com/product-detail/1-Pc-Body-Fat-Tester-Analyzer_1600128381046.html?spm=a27aq.22883793.4119238120.13.2709bda5UKlcmS&ecology_token=default
    '''
    pattern = re.compile(r'\w+\.(com|net)')
    filter = pattern.finditer(text)
    for match in filter:
        print(match)

if __name__ == '__main__':
    find_site(URL)
