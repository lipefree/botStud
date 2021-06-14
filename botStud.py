import discord
from discord.ext import commands, tasks
import youtube_dl
import os
import asyncio

intents = discord.Intents().default()
intents.voice_states = True
client = commands.Bot(command_prefix="!",intents=intents)

#cogs organisation

initital_extensions = ['cogs.studyRoom']

#cogs loading

if __name__ == '__main__':
    for extension in initital_extensions :
        client.load_extension(extension)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    checkIfAlone.start()

@tasks.loop(seconds = 10)
async def checkIfAlone():
    if len(client.voice_clients) is not 0 :
        if len(client.voice_clients[0].channel.members) == 1 :
            await client.voice_clients[0].disconnect()


print("working")

client.run('ODUyMjg3OTU4MDA2NzU5NDU0.YMEpAw.PbpJJTb8BElFk6Qaj9PkY1H1O-4')
