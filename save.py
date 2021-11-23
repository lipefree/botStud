import discord
from discord.ext import commands
import os
import youtube_dl
import datetime
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
    }

ffmpeg_options = {
    'options': '-vn'
    }

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

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

    @commands.command(name='test')
    async def test(self, ctx):
        message = f"[{datetime.datetime.now()}] test by {ctx.author.name}"
        print(message)
        await ctx.send(message)

    @commands.command(name='join')
    async def join(self, ctx):
        """Joins a voice channel"""
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        await voice.connect()

    @commands.command(name='play')
    async def play(self, ctx, url : str):


        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

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
        # song_there = os.path.isfile("song.webm")
        # try:
        #     if song_there:
        #         os.remove("song.webm")
        # except PermissionError:
        #     print("error") 

        # ydl_opts = {
        #     'format' : '249/250/251'
        # }
        # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #     ydl.download([url])
        # for file in os.listdir("./"):
        #     if file.endswith(".webm"):
        #         os.rename(file, "song.webm")
        pass
        

    def is_connected(self):
        voice = discord.utils.get(self.client.voice_clients, guild = 852120040588967946)
        return voice and voice.is_connected

def setup(client):
    client.add_cog(StudyRoomCog(client))

