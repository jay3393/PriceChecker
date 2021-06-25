'''
Module to display information on console
'''
import datahandler

class Display:

    def __init__(self):
        self.console_log = ""
        #self.packer = datahandler.Package(self.name, self.price, self.url, self.store)

    def generate_console_log(self, name, price, url, store):
        self.console_log += "==================================================\n"
        self.console_log += (f'Product >> {name}\n')
        self.console_log += (f'Store >> {store}\n')
        self.console_log += (f'Price >> {price}\n')
        self.console_log += (f'Link >> {url}\n')
        self.console_log += ('==================================================\n')

    def print_console_log(self):
        print(self.console_log)
        self.console_log = ""