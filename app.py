from datetime import date, datetime
import discord
import os

from discord import message
from discord import channel
from discord import voice_client
from ytdl import YTDLSource
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Constants

DISCORD_TOKEN = os.getenv('discord_token')
COMMAND_PREFIX = os.getenv('command_prefix')

# Bot configuration

intents = discord.Intents().all()
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = COMMAND_PREFIX, client = client)

# Bot events

@bot.event
async def on_ready():
    print("The bot is configured and ready to work!")

# Bot commands

@bot.command(name = 'play', help = 'Tells the bot to play the song')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        # Joins voice channel if not yet
        if not voice_channel:
            await join(ctx)
            voice_channel = server.voice_client

        async with ctx.typing():
            audio_info = await YTDLSource.from_url(url, loop = bot.loop)
            audio = discord.FFmpegOpusAudio(source = audio_info.filename, executable = "./ffmpeg")
            voice_channel.play(audio)
        
        embed = discord.Embed(
            title = audio_info.title,
            url = url,
            color = discord.Color.blue()
        )
        if audio_info.duration:
            embed.add_field(name = "Duration", value = audio_info.duration, inline = True)
        
        await ctx.send(embed = embed)
    
    except Exception as e:
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