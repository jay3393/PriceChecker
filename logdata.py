'''
Data saving/loading
Takes the data in JSON form from main component and update changed values of prices.
'''
import json
import os

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
        if not self.savefile:
            with open(self.savefile, 'w') as f:
                print('Initializing log...')
            f.close()
        if os.stat(self.savefile).st_size == 0:
            print("Empty log found! Dumping data...")
            with open(self.savefile, 'w') as f:
                json.dump(self.data, f, sort_keys=False, indent=4)
            f.close()
        else:
            print("Updating product list...")
            # Retrieves the current price from the old data set and updates the new data set
            temp = {}
            with open(self.savefile, 'r') as f:
                olddata = json.load(f)['products']
                for product in olddata:
                    name = product['name']
                    previousPrice = product['currentPrice']
                    temp[name] = previousPrice

                # Updates the previous price for the new data set
                for product in self.data['products']:
                    product['previousPrice'] = temp.get(product['name'], 'N/A')

            with open('temp.json', 'w') as f:
                json.dump(self.data, f, sort_keys=False, indent=4)
            f.close()

            oldfile = self.savefile
            os.remove(oldfile)
            newfile = 'temp.json'
            os.rename(newfile, oldfile)

            print("List updated!")