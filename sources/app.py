import discord
import os

from discord import player
from discord.ext import commands
from dotenv import load_dotenv
from engines.ytdl import YTDLSource
from utils.player import Player

load_dotenv()

# Constants

DISCORD_TOKEN = os.getenv('discord_token')
COMMAND_PREFIX = os.getenv('command_prefix')

# Bot configuration

intents = discord.Intents().all()
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = COMMAND_PREFIX, client = client)

# Player configuration

player = Player(bot)

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
        
        player.play_song(ctx, voice_channel, url)
    
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
    player.add_song_to_queue(url)

@bot.command(name = 'clear', help = "Removes all tracks from the current queue")
async def clear(ctx):
    if player.current_queue():
        player.clear_queue()
        await ctx.send("Queue has been cleared")
    else:
        await ctx.send("Queue is empty already")

@bot.command(name = 'show_queue', help = "Shows list of tracks from the current queue")
async def show_queue(ctx):
    description = ""
    for (index, song) in enumerate(player.current_queue()):
        description += "{}. {}\n".format(index + 1, YTDLSource.get_info(song).title)
    embed = discord.Embed(
        title = "Playlist",
        description = description or "There are no songs in the queue currently 😴",
        color = discord.Color.blue()
    )
    await ctx.send(embed = embed)

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