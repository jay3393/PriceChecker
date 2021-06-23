'''
Data saving/loading
Takes the data in JSON form from main component and update changed values of prices.
'''
import json

class UpdateLog:
    '''Description'''

    def __init__(self, data):
        self.savefile = 'productHistory.json' # Change file if needed
        self.data = data

    # This is to test functionality, change later to save json to csv file
    def key_exists(self, key):
        with open(self.savefile, 'r') as f:
            data = json.loads(f)
        return True if key in data else False

    def update(self):
        temp = {}
        with open(self.savefile, 'r') as f:
            olddata = json.load(f)['products']
            for product in olddata:
                name = product['name']
                previousPrice = product['currentPrice']
                temp[name] = previousPrice

            for product in self.data['products']:
                product['previousPrice'] = temp.get(product['name'])

        
        f.close()

    def tempUpdate(self):
        with open(self.savefile, 'w') as f:
            json.dump(self.data, f, indent=4, sort_keys=False)
        f.close()