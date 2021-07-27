import initialize

textfile = 'products.txt'
delay = 60 # delay in minutes
jsonfile = 'productHistory.json'

if __name__ == '__main__':
    print('==============================Running price checker==============================')
    initialize.__init__(textfile, delay)