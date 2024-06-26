# discord-bot

## Setup

### Discord Developer Application

1. Go [Discord Developer Portal](https://discord.com/developers/applications).
2. Create an application.
3. Generate a token and paste on `bot.py`.
   > Bot (SETTINGS) → Build-A-Bot → TOKEN
   >
   > bot.py
   >
   > ```py
   > import discord
   > from discord.ext import commands
   >
   > TOKEN = "YOUR_TOKEN"
   > ...
   > ```
4. Set `MESSAGE CONTENT INTENT` on.
   > Bot (SETTINGS) → Privileged Gateway Intents → MESSAGE CONTENT INTENT
5. Invite the bot to your server.

### discord.py

https://discordpy.readthedocs.io/en/stable/intro.html

`python3 -m pip install -U discord.py[voice]`

> for linux environments
>
> `sudo apt install libffi-dev libnacl-dev python3-dev`

### Google Text-to-Speech

https://github.com/pndurette/gTTS

`pip install gTTs`

> for linux environments
>
> `sudo apt install ffmpeg`
