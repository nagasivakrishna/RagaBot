import os
import discord
import youtube_dl
# from bs4 import BeautifulSoup
from discord.ext import commands
from youtube_search import YoutubeSearch
from keep_alive import keep_alive
my_secret = os.environ['TOKEN']


client = commands.Bot(command_prefix="!!")
@client.command()
async def on_message(message):
  if message.content.startswith("!!play"):
    songReq = message.split(" ")
    print(songReq)

@client.command()
async def play(ctx, url : str):
  if  '://' in url or 'www' in url:

    song_there = os.path.isfile("song.mp3")
    try:
      if song_there:
        os.remove("song.mp3")
    except PermissionError:
      await ctx.send("stop the song first or use add :) ")
      return
    
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    
    voiceclient = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voiceclient is not None:
      voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    else:
      await voiceChannel.connect()
      voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
      
      
    ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
      }]
    }
    
    if song_there:
      await ctx.send("Hol up! it takes time. ")
      await stop(ctx)
      await play(ctx, url)
    else:
      await ctx.send("Hol up! it takes time. ")
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
      for file in os.listdir("./"):
        if file.endswith(".mp3"):
          os.rename(file, "song.mp3")
      voice.play(discord.FFmpegPCMAudio("song.mp3"))
      await ctx.send("Playing your song")
  else:
    results = YoutubeSearch(f'{url.replace(" ", "")}', max_results=1).to_dict()
    print(url.replace(" ", ""))
    url = f'https://www.youtube.com{results[0]["url_suffix"]}'
    await play(ctx, url)

@client.command()
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_connected():
    await voice.disconnect()
  else:
    await ctx.send("Not Connected!")

@client.command()
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("Not playing any music.")

@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if not voice.is_playing():
    voice.resume()
  else:
    await ctx.send("Already playing music.")

@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()

keep_alive()
client.run(my_secret)