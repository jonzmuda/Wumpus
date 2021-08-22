#Imports

from discord.ext import commands
import discord
import os
from discord.ext.commands import bot
from dotenv import load_dotenv
import asyncio
import random
import json

load_dotenv()

#Variables

Prefix = os.getenv("Prefix")
Name = os.getenv("Name")
Owners = os.getenv("Owners")

#Load Cog

class Template(commands.Cog, name="Template"):
    def __init__(self, bot):
        self.bot = bot


#Setup Cog

def setup(bot):
    bot.add_cog(Template(bot))