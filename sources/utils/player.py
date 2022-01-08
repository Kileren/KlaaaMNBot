import asyncio
import discord

from discord.ext.commands.bot import Bot
from engines.ytdl import YTDLSource

# https://stackoverflow.com/a/62114462
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Player:

    __bot: Bot
    __songs_queue = list()

    def __init__(self, bot: Bot):
        self.__bot = bot

    def play_song(self, ctx, client, url):
        audio_info = YTDLSource.get_info(url)
        audio = discord.FFmpegOpusAudio(source = audio_info.url, bitrate = 320, executable = "./ffmpeg", before_options = FFMPEG_OPTIONS)
        
        def after(error):
            if self.__songs_queue:
                song = self.__songs_queue.pop(0)
                self.play_song(ctx, client, song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.__bot.loop)

        client.play(audio, after = after)

        embed = discord.Embed(
            title = audio_info.title,
            url = url,
            color = discord.Color.blue()
        )
        if audio_info.duration:
            embed.add_field(name = "Duration", value = audio_info.duration, inline = True)
        
        asyncio.run_coroutine_threadsafe(ctx.send(embed = embed), self.__bot.loop)

    def add_song_to_queue(self, url):
        self.__songs_queue.append(url)
    
    def clear_queue(self):
        self.__songs_queue.clear()
    
    def current_queue(self):
        return self.__songs_queue