import asyncio
import json
import os
import platform
import random
import sys
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import datetime
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()

bot = Bot(command_prefix=os.getenv("Prefix"), intents=intents)
Token = os.getenv("Token")
Prefix = os.getenv("Prefix")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"----------------------------")
    status_task.start()

#Status
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = [f"{Prefix}commands", f"{Prefix}info", f"{Prefix}help", f"{Prefix}navigate", f"{Prefix}format"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))
    

bot.remove_command("help")

#Load Cogs

if __name__ == "__main__":
    for file in os.listdir("./Cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"Cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

bot.run(Token)