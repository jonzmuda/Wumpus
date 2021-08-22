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


@bot.event
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

@bot.event
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

@bot.event
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

@bot.event
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

@bot.event
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


bot.run(Token)