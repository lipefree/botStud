import discord
from discord.ext import commands
import os
import youtube_dl
import datetime

class StudyRoomCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    #Detection si qqn se connecte a un channel

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
            if before.channel != after.channel and not self.is_connected():

                voiceChannel = after.channel
                
                guild = self.client.get_guild(852120040588967946)
                
                if(after.channel.id == 852210893780942918): #Cas Lofi
                    # "https://www.youtube.com/watch?v=tNTmJBSXFqc"
                    
                    self.dowloadingSongs("https://www.youtube.com/watch?v=tNTmJBSXFqc")

                    await voiceChannel.connect() #Bot join channel
                    voice = discord.utils.get(self.client.voice_clients, guild = guild)
                    voice.play(discord.FFmpegOpusAudio(executable="H:/ffmpeg-N-102723-g94af6414ab-win64-gpl-shared/bin/ffmpeg", source="song.webm"))


    @commands.command(name='ping')
    async def ping(self, ctx):
        message = f"[{datetime.datetime.now()}] ping by {ctx.author.name}"
        print(message)
        await ctx.send(message)

    @commands.command(name='play')
    async def play(self, ctx, url : str):

        self.dowloadingSongs(url)

        name = ctx.author._get_channel

        #how to select channel
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = 'Salon') #Pour l'instant se connecte a "Salon"

        await voiceChannel.connect() #Bot join channel

        #Voice channel 
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        voice.play(discord.FFmpegOpusAudio(executable="H:/ffmpeg-N-102723-g94af6414ab-win64-gpl-shared/bin/ffmpeg", source="song.webm"))

    @commands.command()  
    async def leave(self, ctx): #Disconnection from channel manually
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_connected:
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("No audio is playing, can't pause")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused, can't resume")

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        voice.stop()

    def dowloadingSongs(self, url):
        song_there = os.path.isfile("song.webm")
        try:
            if song_there:
                os.remove("song.webm")
        except PermissionError:
            print("error") 

        ydl_opts = {
            'format' : '249/250/251'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".webm"):
                os.rename(file, "song.webm")

    def is_connected(self):
        voice = discord.utils.get(self.client.voice_clients, guild = 852120040588967946)
        return voice and voice.is_connected

def setup(client):
    client.add_cog(StudyRoomCog(client))

