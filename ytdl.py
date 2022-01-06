import asyncio
from datetime import datetime
import discord
import youtube_dl

from dataclasses import dataclass
from tokenize import String
from typing import Optional

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': './Music' + '/%(title)s.%(ext)s',
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

@dataclass
class AudioInfo:
    title: str
    filename: str
    duration: Optional[str]

    def __init__(self, title: str, filename: str, duration: Optional[str] = None):
        self.title = title
        self.filename = filename
        self.duration = duration

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        title = data['title']
        filename = title if stream else ytdl.prepare_filename(data)
        duration = format_duration(int(data['duration'])) if 'duration' in data else None
        return AudioInfo(title, filename, duration)

def format_duration(duration: int) -> str:
    add_zero_if_needed = lambda value: value if value >= 10 else "0" + str(value)
    if duration >= 60:
        min = int(duration / 60)
        sec = duration % 60
        return "{}:{}".format(add_zero_if_needed(min), add_zero_if_needed(sec))
    else:
        return add_zero_if_needed(duration)