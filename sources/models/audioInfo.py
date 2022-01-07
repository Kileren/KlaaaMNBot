from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioInfo:
    title: str
    url: str
    duration: Optional[str]

    def __init__(self, title: str, url: str, duration: Optional[str] = None):
        self.title = title
        self.url = url
        self.duration = duration