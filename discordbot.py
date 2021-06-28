import discord
import os
import datahandler
import display
import json
import requests
import validators

token = os.environ.get('SLOWAFBOTTOKEN')

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}

class DiscordBot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def update(self, message):
        '''
        Takes in the message id and returns the data to the message's channel
        '''
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
        f.close()
        await message.channel.send(file=discord.File('sendfile.txt'))

    async def add_product(self, message):
        content = message.content.split()
        if len(content) != 2:
            return
        url = content[1]
        valid_url = validators.url(url)
        if valid_url:
            with open('products.txt', 'a') as f:
                writer = f.write(url + '\n')
            f.close()
            await message.channel.send(f"Now tracking {url}")
            await message.delete()
        else:
            await message.channel.send(f"Invalid URL. Use ?track URL")
        return

    async def remove_product(self, message):
        print("remove product")
        content = message.content.split()
        if len(content) != 2:
            return
        url = content[1]
        valid_url = validators.url(url)
        if valid_url:
            with open('products.txt', 'r') as f:
                lines = f.readlines()
            f.close()
            with open('productstemp.txt', 'w') as w:
                for line in lines:
                    print(line)
                    if line.strip() != url:
                        w.writelines(line.strip())
            await message.channel.send(f"Stopped tracking {url}")
            await message.delete()
        else:
            await message.channel.send(f"Invalid URL. Use ?track URL")

        oldfile = 'products.txt'
        os.remove(oldfile)
        newfile = 'productstemp.txt'
        os.rename(newfile, oldfile)

        return

    async def show_products(self, message):
        embed = discord.Embed(title='Products Tracked',description='     ?track URL to keep track of product prices\n     ?untrack to remove product from being tracked',color=0xebc252)
        with open('products.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                embed.add_field(name=line,value='\u200b',inline=False)
            await message.channel.send(embed=embed)
        f.close()
        return

    async def help(self, message):
        await message.channel.send("Change to embedded")

    async def case_switch(self, content, message):
        task = content[0]
        switcher = {
            '?update': self.update,
            '?track': self.add_product,
            '?products': self.show_products,
            '?untrack': self.remove_product,
            '?helpme': self.help,
        }
        func = switcher.get(task, 'Invalid function')
        if func != 'Invalid function':
            return await func(message)

    async def on_message(self, message):
        # Ignore if the message was from the bot itself
        if message.author == client.user:
            return

        if message.content[0] != '?':
            return print("Not a command")

        content = message.content.split()
        print(content)
        if len(content) > 2:
            return message.channel.send("Invalid parameters, use ?helpme")

        await self.case_switch(content, message)

client = DiscordBot()
client.run(token)