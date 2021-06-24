import initialize

textfile = 'products.txt'
delay = 0.1
jsonfile = 'productHistory.json'

if __name__ == '__main__':
    print('Running price checker...')
    initialize.__init__(textfile, delay)