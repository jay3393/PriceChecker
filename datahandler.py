import json

class Package:

    def __init__(self):
        self.data = {
            "products": []
        }

    def __print__(self):
        '''Overrides print function'''
        print(self.data)

    def pack(self, name, price, url, store):
        '''
        Packs data into JSON formatting and unpack at logdata.py
        '''

        product = {
            "name": name,
            "store": store,
            "currentPrice": price,
            "previousPrice": 'N/A',
            "url": url
        }

        self.data['products'].append(product)

    def unpack(self, filename):
        print(filename)
        with open(filename, 'r') as f:
            data = json.load(f)['products']
            print(data)
        temp = {}
        for item in data:
            name = item['name']
            store = item['store']
            current = item['currentPrice']
            previous = item['previousPrice']
            url = item['url']
            #temp[name] = [store, current, previous, url]
            temp[name] = {
                "store": store,
                "currentPrice": current,
                "previousPrice": previous,
                "url": url
            }
            print(temp)

        return temp