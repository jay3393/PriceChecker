'''
Data saving/loading
Takes the data in JSON form from main component and update changed values of prices.
'''
import json
import csv

class UpdateLog:

    # textfile = 'product_history.txt'
    #
    # def update(self, data):
    #     data1 = ['1','2','3','4','5']
    #     data2 = ['one','two','three','four','five']
    #     with open(self.textfile, 'a') as f:
    #         csv_writer = csv.writer(f, delimiter=',')
    #         csv_writer.writerow(data)

    def update(self, data):
        value = json.loads(data)
        for i in value:
            name = i['name']
            price = i['currentPrice']
            store = i['store']
            print("==================================================\n")
            print(f'Product >> {name}\n')
            print(f'Price >> {price}\n')
            print(f'Link >> {store}\n')
            print('==================================================\n')

# if True:
#     updates = UpdateLog()
#     updates.update('abc')