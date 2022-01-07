import asyncio
import discord
import os

from datetime import date, datetime
from discord import channel
from discord import message
from discord import voice_client
from discord.ext import commands
from dotenv import load_dotenv
from http import server
from types import coroutine
from youtube_dl import main
from engines.ytdl import YTDLSource

load_dotenv()

# Constants

DISCORD_TOKEN = os.getenv('discord_token')
COMMAND_PREFIX = os.getenv('command_prefix')

# https://stackoverflow.com/a/62114462
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

# State

songs_queue = list()

# Bot configuration

intents = discord.Intents().all()
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = COMMAND_PREFIX, client = client)

# Bot events

@bot.event
async def on_ready():
    print("The bot is configured and ready to work!")

# Bot commands

def play_song(ctx, client, url):
    audio_info = YTDLSource.get_info(url)
    audio = discord.FFmpegOpusAudio(source = audio_info.url, executable = "./ffmpeg", before_options = FFMPEG_OPTIONS)

    def after(error):
        if songs_queue:
            song = songs_queue.pop(0)
            play_song(ctx, client, song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(audio, after = after)

    embed = discord.Embed(
        title = audio_info.title,
        url = url,
        color = discord.Color.blue()
    )
    if audio_info.duration:
        embed.add_field(name = "Duration", value = audio_info.duration, inline = True)    
    
    asyncio.run_coroutine_threadsafe(ctx.send(embed = embed),  bot.loop)

@bot.command(name = 'play', help = 'Tells the bot to play the song')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        # Joins voice channel if not yet
        if not voice_channel:
            await join(ctx)
            voice_channel = server.voice_client

        play_song(ctx, voice_channel, url)
    
    except Exception as e:
        print(e)
        await ctx.send("The bot is not connected to a voice channel")

@bot.command(name = "pause", help = "Pauses the playing song")
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment")

@bot.command(name = 'resume', help = 'Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("There are no paused songs at the moment")

@bot.command(name = 'stop', help = 'Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment")

@bot.command(name = 'queue', help = "Puts the song in the queue")
async def queue(ctx, url):
    songs_queue.append(url)

@bot.command(help = 'Tells the bot to join the voice channel')
async def join(ctx):
    # Checks that user who wants to play music has joined the voice channel
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to the voice channel".format(ctx.message.authr.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    
    await channel.connect()

@bot.command(name = 'leave', help = 'To make the bot leaves the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel")

# Run bot

bot.run(DISCORD_TOKEN)