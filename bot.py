import discord
from discord.ext import commands


TOKEN = ""

bot = commands.Bot(command_prefix="/")

@bot.event
async def on_ready():
    print("bot on")

bot.run(TOKEN)
