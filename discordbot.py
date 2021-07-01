import discord
import os
import datahandler
import display
import json
import requests
import validators
import sitehandler
import re
import threading
import asyncio
import time

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
            if await self.check_url(url):
                if not await self.contains_url(url):
                    with open('products.txt', 'a') as f:
                        writer = f.write(url + '\n')
                    f.close()
                    await message.channel.send(f"Now tracking {url}")
                    await message.delete()
                else:
                    await message.channel.send(f"URL is already being tracked")
            else:
                await message.channel.send(f"Website is currently not supported")
        else:
            await message.channel.send(f"Invalid URL. Use ?track URL")
        return

    async def remove_product(self, message):
        content = message.content.split()
        if len(content) != 2:
            return
        url = content[1]
        print(f"Untracking product: {url}")
        valid_url = validators.url(url)
        if valid_url:
            with open('products.txt', 'r') as f:
                lines = f.readlines()
            f.close()
            with open('productstemp.txt', 'w') as w:
                for line in lines:
                    print(line)
                    if line.strip() != url:
                        w.writelines(line.strip()+'\n')

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
        embed = discord.Embed(title='Commands', color=0xebc252)
        embed.add_field(name='?helpme',value='Shows the available commands',inline=False)
        embed.add_field(name='?update', value='Lists the prices of each product tracked', inline=False)
        embed.add_field(name='?products', value='Lists the products being tracked', inline=False)
        embed.add_field(name='?track', value='Adds the product to tracking list', inline=False)
        embed.add_field(name='?untrack', value='Removes the product from tracking list', inline=False)
        await message.channel.send(embed=embed)

    async def contains_url(self, URL):
        retval = False
        with open('products.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() == URL:
                    retval = True
        return retval

    async def check_url(self, URL):
        '''
        Calls the function for the matching URL
        Add switcher element when adding new site
        '''
        pattern = re.compile(r'\w+\.(com|net)')
        filter = pattern.search(URL)
        print(filter)
        arg = str(filter.group())
        switcher = {
            'bestbuy.com': 'Supported',
            'walmart.com': 'Supported',
            'microcenter.com': 'Supported',
        }
        func = switcher.get(arg, lambda: 'Website not supported')
        if func == 'Supported':
            print("supported")
            return True
        else:
            print("unsupported")
            return False

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

    async def price_change(self,packet):
        channel = client.get_channel(403812490112139265)
        body = ''
        embed = discord.Embed()
        for data in packet:
            name = data['name']
            url = data['url']
            current = data['currentPrice']
            previous = data['previousPrice']
            change = abs(float(current.strip('$')) - float(previous.strip('$')))
            change = "{:.2f}".format(change)
            body += previous + ' -> ' + current + ' ($' + change + ')' + '\n' + url + '\n'
            embed.add_field(name=name, value=body, inline=False)

        await channel.send(embed=embed)

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
def run_client():
    asyncio.run(client.run(token))

def something(packet):
    print('started something')
    loop = asyncio.get_event_loop()
    asyncio._set_running_loop(loop)
    task = asyncio.create_task(client.price_change(packet))

x = threading.Thread(target=run_client)
x.start()