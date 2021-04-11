import discord
import asyncio
import json
import random
import os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests

client = discord.Client()



with open('data.json', 'r') as f:
    data = json.load(f)

with open('coin.json', 'r') as f:
    coin = json.load(f)





@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('김민수'))

@client.event
async def on_message(message):


        if message.content.startswith("제리야 배워"):
            i = message.content[7:].split("/")
            if i[0] in data:
                data[i[0]].append(i[1])
                coin[str(message.author.id)][0] += 300
            else:
                data[i[0]] = [i[1]]
                coin[str(message.author.id)][0] += 300

            await message.channel.send("아주~ 잘 배웠음")


    
        await asyncio.sleep(random.randrange(4, 6))





client.run(os.environ['token'])
