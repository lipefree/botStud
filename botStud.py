#!/usr/bin/env python3

import discord
from discord.ext import commands, tasks
import youtube_dl
import os
import asyncio
import DiscordToken
from cogs.StudyRoom import Music

# intents = discord.Intents().default()
# intents.voice_states = True
# client = commands.Bot(command_prefix="!",intents=intents)

#cogs organisation

# initital_extensions = ['cogs.studyRoom']

#cogs loading

# if __name__ == '__main__':
#     for extension in initital_extensions :
#         client.load_extension(extension)

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#     checkIfAlone.start()

# @tasks.loop(seconds = 10)
# async def checkIfAlone():
#     if len(client.voice_clients) != 0 :
#         if len(client.voice_clients[0].channel.members) == 1 :
#             await client.voice_clients[0].disconnect()

# print("working")

# @commands.command(name='version')
#     async def version(self, ctx):
#         message = f"[{datetime.datetime.now()}] version by {ctx.author.name}\n"
#         message += subprocess.run(["git", "log", "-1"], cwd="/home/llama/botStud", capture_output=True).stdout.decode('unicode_escape')
#         print(message)
#         await ctx.send(message)

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(Music(bot))
bot.run(DiscordToken.TOKEN)

# client.run(DiscordToken.TOKEN)

