class Product:

    def __init__(self, name, price, url, store):
        self.name = name
        self.price = price
        self.url = url
        self.store = store

    def disassemble(self):
        return self.name, self.price, self.url, self.store

    def __print__(self):
        print(f'Name: {self.name}')
        print(f'Price: {self.price}')
        print(f'Store: {self.store}')
        print(f'URL: {self.url}')