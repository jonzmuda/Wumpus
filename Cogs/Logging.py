#Imports

from discord.ext import commands
import discord
import os
from discord.ext.commands import bot
from dotenv import load_dotenv
import asyncio
import random
import json
import datetime

load_dotenv()

#Variables

Prefix = os.getenv("Prefix")
Name = os.getenv("Name")
Owners = os.getenv("Owners")

#Load Cog

class Template(commands.Cog, name="Template"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(message):
        if message.author == bot.user or message.author.bot:
            return
        elif len(message.clean_content) > 50:
            await message.channel.send("That message is way to long!\nQuickly copy your message before it gets deleted and send it here \nhttps://pastebin.com/")
            await asyncio.sleep(5)
            await message.delete()
        elif not (await bot.get_context(message)).valid and len(message.content) <= 50:
            Message_Logs = bot.get_channel(878725254200041533)
            embed = discord.Embed(
            title=f"New Message", color=0xE02B2B)
            embed.add_field(name="Author:", value=f"{message.author.mention}", inline=True)
            embed.add_field(name="Channel:", value=f"{message.channel.mention}", inline=True)
            embed.add_field(name="Content:", value=f"{message.content}", inline=False)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await Message_Logs.send(embed=embed)
        await bot.process_commands(message)
    
    @commands.Cog.listener()
    async def on_message_delete(message):
        Other_Logs = bot.get_channel(878730086088585217)    
        embed = discord.Embed(
        title=f"Deleted Message", color=0xE02B2B)
        embed.add_field(name="Author:", value=f"{message.author.mention}", inline=True)
        embed.add_field(name="Channel:", value=f"{message.channel.mention}", inline=True)
        embed.add_field(name="Content:", value=f"{message.content}", inline=False)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await Other_Logs.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_edit(message_before, message_after):
        Other_Logs = bot.get_channel(878730086088585217)    
        embed = discord.Embed(
        title=f"Deleted Message", color=0xE02B2B)
        embed.add_field(name="Author:", value=f"{message_before.author.mention}", inline=True)
        embed.add_field(name="Channel:", value=f"{message_before.channel.mention}", inline=True)
        embed.add_field(name="Original:", value=f"{message_before.content}", inline=False)
        embed.add_field(name="Updated:", value=f"{message_after.content}", inline=False)
        embed.set_thumbnail(url=message_before.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await Other_Logs.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_completion(ctx):
        fullCommandName = ctx.command.qualified_name
        split = fullCommandName.split(" ")
        executedCommand = str(split[0])
        Command_Logs = bot.get_channel(878440647848255488)    
        embed = discord.Embed(
        title=f"Command Executed", color=0xE02B2B)
        embed.add_field(name="Author:", value=f"{ctx.message.author.mention}", inline=True)
        embed.add_field(name="Channel:", value=f"{ctx.channel.mention}", inline=True)
        embed.add_field(name="Command:", value=f"{executedCommand}", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await Command_Logs.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_error(context, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                title="Hey, please slow down!",
                description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error!",
                description="You are missing the permission `" + ", ".join(
                    error.missing_perms) + "` to execute this command!",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                description=str(error).capitalize(),
                color=0xE02B2B
            )
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Command Not Found!",
                description="The command you tried to execute was not found!",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        raise error

#Setup Cog

def setup(bot):
    bot.add_cog(Template(bot))