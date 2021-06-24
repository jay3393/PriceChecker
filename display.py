'''
Module to display information on console
'''
import datahandler

class Display:

    def __init__(self, name, price, url, store):
        self.name = name
        self.price = price
        self.url = url
        self.store = store
        self.console_log = ""
        self.packer = datahandler.Package(self.name, self.price, self.url, self.store)

    def generate_console_log(self):
        self.console_log += "==================================================\n"
        self.console_log += (f'Product >> {self.name}\n')
        self.console_log += (f'Store >> {self.store}\n')
        self.console_log += (f'Price >> {self.price}\n')
        self.console_log += (f'Link >> {self.url}\n')
        self.console_log += ('==================================================\n')

        self.packer.name = self.name
        self.packer.price = self.price
        self.packer.url = self.url
        self.packer.store = self.store

        self.packer.pack()

    def print_console_log(self):
        print(self.console_log)
        self.console_log = ""