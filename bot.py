import discord
from discord.ext import commands

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
    if msg.guild is None:
        return

    global guild_channels
    channel_id = guild_channels.get(msg.guild.id)
    if msg.channel.id == channel_id and msg.author != bot.user:
        name = msg.author.nick or msg.author.global_name or msg.author.name
        print(name, msg.content)

    await bot.process_commands(msg)


@bot.command()
async def set(ctx):
    global guild_channels
    guild_channels[ctx.guild.id] = ctx.channel.id
    await ctx.send(f"set channel ({ctx.channel.name})")


bot.run(TOKEN)
