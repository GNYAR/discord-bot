import discord
from discord.ext import commands

TOKEN = "YOUR_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

channel = None


@bot.event
async def on_ready():
    print("bot on")


@bot.event
async def on_message(msg):
    global channel
    if msg.channel == channel and msg.author != bot.user:
        name = msg.author.nick or msg.author.global_name or msg.author.name
        print(name, msg.content)

    await bot.process_commands(msg)


@bot.command()
async def set(ctx):
    global channel
    channel = bot.get_channel(ctx.channel.id)
    await channel.send(f"set channel ({ctx.channel.name})")


bot.run(TOKEN)
