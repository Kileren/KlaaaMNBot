# KlaaaMNBot

![Python](https://img.shields.io/badge/python-3.9.9-yellow)

Bot for playing music in discord channels.
Supported sources:
| Source        | Supports      |
|:--------------|:-------------:|
| YouTube       | ✅           |
| Spotify       | ❌           |
| SoundCloud    | ❌           |

## Getting Started

1. Firstly you need to create your bot on [discord developers portal](https://discord.com/developers/applications) to get your own token. You can follow this [instruction](https://trustedmercury.medium.com/how-to-make-a-discord-bot-with-python-e066b03bfd9) in order to catch up a basics.
2. Open `.env` file and fill `discord_token` property with the token you got on the previous step.
3. Make sure you installed all needed dependencies (file `requirements.txt`). To do that fast way you can run `python3 -m pip install -r requirements.txt` in terminal, it will install all dependencies from `requirements.txt` file.
4. Bot uses [FFmpeg](https://www.ffmpeg.org) to play the music. You need to download the executable file from the [official site](https://www.ffmpeg.org) according to your OS and place that file in the root folder of KlaaaMNBot. Otherwise, the bot won't be able to play music and will respond to each attempt with an error.  
**IMPORTANT: the name of the file should be `ffmpeg`**
5. One last step - run the bot. You can do this by running `sh start.sh` in terminal or manually by executing `python3 sources/app.py`. Both commands are valid from the bot's root folder.
6. You're done! Don't forget to invite bot to your server.

## Attention

This bot should be used only for personal use.  
Also take note on [this article](https://www.techadvisor.com/how-to/internet/is-it-legal-download-youtube-videos-3420353/).