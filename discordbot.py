import discord
import os
import datahandler
import display
import json

token = os.environ.get('SLOWAFBOTTOKEN')

class DiscordBot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        # Ignore if the message was from the bot itself
        if message.author == client.user:
            return

        if message.content == '!update':
            displayer = display.Display()
            with open('productHistory.json', 'r') as f:
                data = json.load(f)['products']
                for product in data:
                    name = product['name']
                    price = product['currentPrice']
                    url = product['url']
                    store = product['store']
                    displayer.generate_console_log(name, price, url, store)
            f.close()
            with open('sendfile.txt', 'w') as f:
                write = f.write(displayer.console_log)
            await message.channel.send(file=discord.File('sendfile.txt'))

client = DiscordBot()
client.run(token)