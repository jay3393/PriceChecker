'''
Data saving/loading
Takes the data in JSON form from main component and update changed values of prices.
'''
import csv

class UpdateLog:

    textfile = 'product_history.txt'

    def update(self, data):
        data1 = ['1','2','3','4','5']
        data2 = ['one','two','three','four','five']
        with open(self.textfile, 'a') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data)

if True:
    updates = UpdateLog()
    updates.update('abc')