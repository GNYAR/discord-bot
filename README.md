# discord-bot

Make discord more convenient.

features: text to speech

## Features

### text to speech

Helping user to speak without microphone.

To use this feature, please join a voice channel and send the message in the specified channel. The bot will join your voice channel automatically.

#### `/langs`

List the languages Google Text-to-Speech supports.

_\<lang>&nbsp;&nbsp;&nbsp;&nbsp;\<name>_

```
af    Afrikaans
am    Amharic
ar    Arabic
...
```

#### `/set`

Set language and the channel to which the command is sent for text-to-speech feature.

**_parameters:_**

**_\<lang>_** a language Google Text-to-Speech supports (default: zh-TW)

#### `/disconnect`

Make the bot disconnect from voice channel

## Setup

- Discord Developer Application
- dotenv
- discord.py
- Google Text-to-Speech

### Discord Developer Application

1. Go [Discord Developer Portal](https://discord.com/developers/applications).
2. Create an application.
3. Generate a token and set environment variable `TOKEN`.
   > Bot (SETTINGS) → Build-A-Bot → TOKEN
   >
   > `.env`
   >
   > ```
   > TOKEN=YOUR_TOKEN
   > ```
4. Set `MESSAGE CONTENT INTENT` on.
   > Bot (SETTINGS) → Privileged Gateway Intents → MESSAGE CONTENT INTENT
5. Invite the bot to your server.

### dotenv

`pip install python-dotenv`

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
