import initialize
import threading
import discordbot

textfile = 'products.txt'
delay = 60 # delay in minutes
jsonfile = 'productHistory.json'

def run():
    initialize.__init__(textfile, delay)


if __name__ == '__main__':
    print('==============================Running price checker==============================')
    # initialize.__init__(textfile, delay)
    x = threading.Thread(target=run)
    x.start()
    discordbot.run_client()