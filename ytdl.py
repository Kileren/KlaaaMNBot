import discord
import youtube_dl
import utils

from Models.audioInfo import AudioInfo

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_options)

class YTDLSource(discord.PCMVolumeTransformer):

    @classmethod
    def get_info(cls, url):
        info = ytdl.extract_info(url, download = False)
        if 'entries' in info:
            info = info['entries'][0]
        title = info['title']
        duration = utils.format_duration(int(info['duration'])) if 'duration' in info else None
        url = info['formats'][0]['url']
        return AudioInfo(title, url, duration)