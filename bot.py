import os
import json

import discord
from discord.ext import commands
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
STORAGE = "guild_vars.json"

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
        # check if user in a voice channel
        if msg.author.voice is not None:
            # connect to the voice channel
            voice_channel = msg.author.voice.channel
            if guild.voice_client is not None:
                await guild.voice_client.move_to(voice_channel)
            else:
                await voice_channel.connect(self_deaf=True)

            # text to speak
            txt = f"{name} 說 {msg.content}"
            audio_name = f"{guild.id}.mp3"
            tts = gTTS(txt, lang=x["tts_lang"])
            tts.save(audio_name)
            guild.voice_client.play(
                discord.FFmpegPCMAudio(audio_name),
                after=lambda e: print(f"Player error: {e}") if e else None,
            )

        else:
            await msg.reply("Please join a voice channel.")

    await bot.process_commands(msg)


@bot.tree.command(description="set channel for tts-bot")
@discord.app_commands.describe(lang="tts language")
async def set(interaction, lang: str):
    global guild_vars
    guild_vars[str(interaction.guild_id)] = {
        "channel_id": interaction.channel_id,
        "tts_lang": lang,
    }

    with open(STORAGE, "w") as f:
        json.dump(guild_vars, f)

    resp = f"Set channel. ({interaction.channel.name}) tts-language: {lang}"
    await interaction.response.send_message(resp)


@bot.tree.command(description="disconnect from voice channel")
async def disconnect(interaction):
    os.remove(f"{interaction.guild_id}.mp3")
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("disconnected.")


bot.run(TOKEN)
