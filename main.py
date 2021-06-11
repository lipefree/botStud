import discord
from discord.ext import commands
import youtube_dl
import os

intents = discord.Intents().default()
intents.voice_states = True
client = commands.Bot(command_prefix="!",intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #a faire -> dowload les musiques au debut

#Detection si qqn se connecte a un channel
@client.event
async def on_voice_state_update(member, before, after):
        if before.channel != after.channel and not is_connected():
            
            #Cas Lofi
            if(after.channel.id == 852210893780942918):
                print("Move to lofi")

                song_there = os.path.isfile("song.webm")
                try:
                    if song_there:
                        os.remove("song.webm")
                except PermissionError:
                    print("error")

                voiceChannel = after.channel
                guild = client.get_guild(852120040588967946)

                await voiceChannel.connect() #Bot join channel

                voice = discord.utils.get(client.voice_clients, guild = guild)

                ydl_opts = {
                    'format' : '249/250/251'
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(["https://www.youtube.com/watch?v=tNTmJBSXFqc"])
                for file in os.listdir("./"):
                    if file.endswith(".webm"):
                        os.rename(file, "song.webm")

                voice.play(discord.FFmpegOpusAudio(executable="H:/ffmpeg-N-102723-g94af6414ab-win64-gpl-shared/bin/ffmpeg", source="song.webm"))


def is_connected():
    voice = discord.utils.get(client.voice_clients, guild = 852120040588967946)
    return voice and voice.is_connected
            
#Commencement coding pour les study rooms

@client.command(name='play')
async def play(ctx, url : str):

    print("triggerd") #testing

    song_there = os.path.isfile("song.webm")
    try:
        if song_there:
            os.remove("song.webm")
    except PermissionError:
        await ctx.send("Wait for current playing music to end or use the 'stop' command")

    #how to select channel
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = 'Salon') #Pour l'instant se connecte a "Salon"

    await voiceChannel.connect() #Bot join channel

    #Voice channel 
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : '249/250/251'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "song.webm")
    voice.play(discord.FFmpegOpusAudio(executable="H:/ffmpeg-N-102723-g94af6414ab-win64-gpl-shared/bin/ffmpeg", source="song.webm"))

@client.command()  
async def leave(ctx): #Disconnection from channel
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_connected:
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx("No audio is playing, can't pause")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused, can't resume")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()

print("working")

client.run('ODUyMjg3OTU4MDA2NzU5NDU0.YMEpAw.5WS9lOabMPnTuQ7ZYWRE7ypp7MY')
