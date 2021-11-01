
# Beta version 1.2  23rd Oct 2021
# Low latency for highly requested song
# queue download System to reduce download latency
# But implementation FFMpeg paralel conversion needed

import os
import discord
import youtube_dl
import asyncio
import random
from discord.ext import commands
from youtube_search import YoutubeSearch
from keep_alive import keep_alive
from downloading import Parallel_Download

# my_secret = os.environ['TOKEN']

client = commands.Bot(command_prefix="!!")
print("[LOG] Dependencies are installed")
req = ""
qu = []
is_playing = False

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192'
        }]
      }

ydl_opts2 = {
        'format': 'bestaudio/best',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
      }

@client.command()
async def join(ctx):
  print("---------------------------------")
  if ctx.author.voice:
    if ctx.voice_client is None or ctx.guild.voice_client.channel != ctx.message.author.voice.channel:
      authchannel = ctx.message.author.voice.channel
      try:
        await authchannel.connect()
        print(f"[JOIN] Bot joined user's channel --> {ctx.guild.voice_client.channel}")
      except:
        await ctx.guild.voice_client.disconnect()
        await authchannel.connect()
      return True
    else:
      print("[JOIN] already connected to the user's channel")
      return True
  else:
    await ctx.send("Connect to a voice channel! ")
    print("[JOIN] User not connected")
    return False
  
@client.command()
async def queue(ctx):
  if len(qu) != 0:
    for i in qu:
          await ctx.send(f"{i}")
  else:
    await ctx.send("No songs in the queue at the moment")


@client.command()
async def play(ctx, url : str):
  print()
  randnum = random.randint(0, 3)
  voice = ctx.message.guild.voice_client
  check = await join(ctx)
  if  'youtube' in url or 'www' in url or 'youtu.be' in url:    
    if voice.is_playing():
      qu.append(f"{url}")
      await ctx.send("Song added to queue!")
      Parallel_Download(url)
      pass
    else:
      print(f"[LOG] User requested --> {url}")
      song_there = os.path.isfile(f"./FILES/{url[24:]}.mp3")

      if check == False:
        print("[LOG] Since user not connected returning 0 status")
        return 

      ###  Youtube Download
      if not song_there:
        Parallel_Download(url)
        ffmpeg_file = discord.FFmpegPCMAudio(f"./FILES/{url[24:]}.mp3")
      
      else:
        ffmpeg_file = discord.FFmpegPCMAudio(f"./FILES/{url[24:]}.mp3")

      ###  Final check to ensure the bot is connected 
      await join(ctx) 
      
      try:
        ctx.voice_client.play(ffmpeg_file)
        print("[LOG] Try case inside the play function with ffmpeg_file has run succesfully")
      ### playing the song
        await ctx.send(f"Now Playing --> {url}")
        print("[LOG] playing the requested song")
      except:  
        print("[ERROR] Failed to process - Bad file descriptor")
        return
      print("--------------END----------------")
  
  else:

    check = await join(ctx)
    req = ctx.message.content[6:]
    print(f"[LOG] Raw text input >> Youtube Search for {req}")

    if check == True:
      ######### -  Random responses
      if randnum == 0:
        await ctx.send("Youtube is very very bad person stops me from doing my job. But i have my ways around ;)")
      elif randnum == 1:
        await ctx.send("Damn! yt is blocking me. But I have a light saber.")
      elif randnum == 2 or randnum == 3:
        await ctx.send("You are cute! I will play your song")
      ######### -  Random responses

      print(f"[LOG] Youtube search is running for {req}")
      results = YoutubeSearch(f'{req.replace(" ", "")}', max_results=1).to_dict()
      
      ### youtube search finding the url
      try:  
        url = f'https://www.youtube.com{results[0]["url_suffix"]}'
      except:
        await ctx.send("Try searching with few words")
      print(f"[LOG] URL changed to {url} --> moving to play function")
      await play(ctx, url)

    else:
      print("[LOG] Since user not connected returning 0 status")
      return
  
  try:
    while voice.is_playing():
      print("---waiting to finish the song")
      await asyncio.sleep(10)
  except:
    print("---Song is finished, moved ahead")
    try:
      await next(ctx)
    except:
      print("[LOG] moved but exception occured at moving to next() function")
      return
  

@client.command()
async def next(ctx):
  try:
    if len(qu) != 0:
      tempval = qu[0]
      qu.remove(qu[0])
      await stop(ctx)
      await play(ctx, tempval)
  except:
    await ctx.send("No song in queue")

@client.command()
async def leave(ctx):
  if ctx.voice_client is not None:
    print(f"[LOG] BOT disconnected from {ctx.guild.voice_client.channel}")
    await ctx.guild.voice_client.disconnect()
  else:
    await ctx.send("Not Connected!")


@client.command()
async def pause(ctx):
  voice = ctx.message.guild.voice_client
  if voice.is_playing():
    ctx.voice_client.pause()
    print("[LOG] BOT Paused")
  else:
    await ctx.send("Not playing any music.")


@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  await join(ctx)
  if not voice.is_playing():
    ctx.voice_client.resume()
    print("[LOG] BOT Resumed playing")
  else:
    await ctx.send("Already playing music.")


@client.command()
async def stop(ctx):
  ctx.voice_client.stop()
  print("[STOP] BOT stopped playing, still in channel")

@client.command()
async def reset(ctx):
  await ctx.send("Resetting!!!")
  await pause(ctx)
  await leave(ctx)
  await join(ctx)
  await asyncio.sleep(3)
  await resume(ctx)

keep_alive()
try:
  print("[LOG] running the client")
  client.run(process.env.TOKEN)
except:
  print("[LOG] Error occured - http 429")
