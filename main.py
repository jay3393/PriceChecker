from bs4 import BeautifulSoup
import time
import requests

print("Enter a ticker")
ticker = input('>').upper()
url = 'https://www.google.com/finance/quote/' + ticker

def initialize():
    r = requests.get(url).text
    bs = BeautifulSoup(r, 'lxml')
    price = bs.find('div', class_='YMlKec fxKbKc')
    if price != None:
        print(f"Checking price of {ticker}...")
        print(f"{ticker.split(':')[0]}   {price.text}")
        return float(price.text.strip('$'))
    else:
        print("Ticker not found")
        return None

def check_price(operation):
    r = requests.get(url).text
    bs = BeautifulSoup(r, 'lxml')
    price = bs.find('div', class_ = 'YMlKec fxKbKc').text.strip('$')
    if float(price) > float(target):
        if operation == '>':
            print(f"{ticker.split(':')[0]} is currently greater than target price {price}")
    if float(price) < float(target):
        if operation == '<':
            print(f"{ticker.split(':')[0]} is currently less than target price {price}")
    print(price)


if __name__ == '__main__':
    price = initialize()
    if price != None:
        print("Set target price")
        target = input('>$')
        print(f"Alert for {ticker.split(':')[0]} set at ${target}")
        operation = '='
        if price > float(target):
            operation = '<'
        else:
            operation = '>'
        while True:
            print("Checking")
            check_price(operation)
            time.sleep(5)
