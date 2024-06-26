import os

import discord
from discord.ext import commands
from gtts import gTTS

TOKEN = "YOUR_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

guild_channels = {}


@bot.event
async def on_ready():
    print("bot on")


@bot.event
async def on_message(msg):
    # ignore direct messages
    if msg.guild is None:
        return

    guild = msg.guild

    # only work on specified channel
    global guild_channels
    channel_id = guild_channels.get(guild.id)
    if msg.channel.id == channel_id and msg.author != bot.user:
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
            tts = gTTS(txt, lang="zh-TW")
            tts.save(audio_name)
            guild.voice_client.play(
                discord.FFmpegPCMAudio(audio_name),
                after=lambda e: print(f"Player error: {e}") if e else None,
            )

        else:
            await msg.reply("Please join a voice channel.")

    await bot.process_commands(msg)


@bot.command()
async def set(ctx):
    global guild_channels
    guild_channels[ctx.guild.id] = ctx.channel.id
    await ctx.send(f"Set channel. ({ctx.channel.name})")


@bot.command()
async def disconnect(ctx):
    global guild_channels
    if ctx.channel.id == guild_channels[ctx.guild.id]:
        os.remove(f"{ctx.guild.id}.mp3")
        await ctx.voice_client.disconnect()


bot.run(TOKEN)
