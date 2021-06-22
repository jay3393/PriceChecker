'''
Data saving/loading
Takes the data in JSON form from main component and update changed values of prices.
'''
import json

class UpdateLog:

    beginning_of_file = 0
    savefile = 'productHistory.json'
    #
    # def update(self, data):
    #     data1 = ['1','2','3','4','5']
    #     data2 = ['one','two','three','four','five']
    #     with open(self.textfile, 'a') as f:
    #         csv_writer = csv.writer(f, delimiter=',')
    #         csv_writer.writerow(data)

    # This is to test functionality, change later to save json to csv file
    def update(self, data):
        with open(self.savefile, "r") as f:
            empty = f.read()
        with open(self.savefile, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=False)
        f.close()