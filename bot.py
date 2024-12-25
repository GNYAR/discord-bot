import os
import json

import discord
from discord.ext import commands
from gtts import gTTS
from gtts.lang import tts_langs
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
STORAGE = "guild_vars.json"


async def join_msg_voice(msg):
    if msg.author.voice is not None:
        # connect to the voice channel
        voice_channel = msg.author.voice.channel
        guild = msg.guild
        if guild.voice_client is not None:
            await guild.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect(self_deaf=True)
        return True
    await msg.reply("Please join a voice channel.")
    return False


def play_audio(guild, filename):
    guild.voice_client.play(
        discord.FFmpegPCMAudio(filename),
        after=lambda e: print(f"Audio player error: {e}") if e else None,
    )


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

guild_channels = {}
guild_vars = {}


@bot.event
async def on_ready():
    global guild_vars
    await bot.tree.sync()

    if os.path.isfile(STORAGE):
        with open(STORAGE, "r") as f:
            guild_vars = json.load(f)
    if guild_vars != {}:
        print("guild_vars loaded")
    else:
        print("guild_vars is empty")

    print("bot on")


@bot.event
async def on_message(msg):
    # ignore direct messages
    if msg.guild is None:
        return

    guild = msg.guild
    global guild_vars
    x = guild_vars.get(str(guild.id))
    # only work on specified channel
    if x and msg.channel.id == x["channel_id"] and msg.author != bot.user:
        name = msg.author.nick or msg.author.global_name or msg.author.name
        if await join_msg_voice(msg):
            # text to speak
            txt = f"{name} 說 {msg.content}"
            audio_name = f"{guild.id}.mp3"
            tts = gTTS(txt, lang=x["tts_lang"])
            tts.save(audio_name)

            play_audio(guild, audio_name)

    await bot.process_commands(msg)


@bot.tree.command(description="languages Google Text-to-Speech supports")
async def langs(interaction):
    lines = list(map(lambda x: "`{}`\t{}".format(*x), tts_langs().items()))
    resp = "\n".join(lines)
    await interaction.response.send_message(resp)


@bot.tree.command(description="set language and channel for text-to-speech")
@discord.app_commands.describe(lang="tts language")
async def set(interaction, lang: str):
    lang_line = f"tts-language: `{lang}`"
    if lang not in tts_langs():
        lang = "zh-TW"
        lang_line = f"lang not found. (default: `{lang}`)"

    global guild_vars
    guild_vars[str(interaction.guild_id)] = {
        "channel_id": interaction.channel_id,
        "tts_lang": lang,
    }

    with open(STORAGE, "w") as f:
        json.dump(guild_vars, f)

    resp = f"Set channel. ({interaction.channel.name})\n{lang_line}"
    await interaction.response.send_message(resp)


@bot.tree.command(description="disconnect from voice channel")
async def disconnect(interaction):
    filename = f"{interaction.guild_id}.mp3"
    if os.path.isfile(filename):
        os.remove(filename)

    if interaction.guild.voice_client is None:
        await interaction.response.send_message("not in any voice channel.")
    else:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("disconnected.")


bot.run(TOKEN)
