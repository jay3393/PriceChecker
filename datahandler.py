import json

class Package:

    def __init__(self, name, price, url, store):
        self.name = name
        self.price = price
        self.url = url
        self.store = store
        self.data = {
            "products": []
        }

    def __print__(self):
        '''Overrides print function'''
        print(self.data)

    def pack(self):
        '''
        Packs data into JSON and unpack at logdata.py
        '''

        product = {
            "name": self.name,
            "store": self.store,
            "currentPrice": self.price,
            "previousPrice": 'N/A',
            "url": self.url
        }

        self.data['products'].append(product)

    def unpack(self):
        data = self.data['products']
        temp = {}
        for item in data:
            name = item['name']
            store = item['store']
            current = item['currentPrice']
            previous = item['previousPrice']
            url = item['url']
            temp[name] = [store, current, previous, url]

        return temp