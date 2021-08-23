import json
from aiohttp.client import request
import discord
from discord.ext import commands
import datetime
import random
import asyncio
import aiohttp
from discord.ext.commands.cooldowns import BucketType
class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say", aliases=["speak", "echo", "repeat", "simonsays", "talk"])
    async def say(self, ctx, arg):
        embed = discord.Embed(
            title=f"{ctx.author} Says", description=f'"{arg}"', color=0xE02B2B)
        embed.set_thumbnail(url="https://i.ibb.co/zbTSLWN/Wumpus-Avatar.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
    
    @commands.command(name="rps")
    async def rock_paper_scissors(self, context):
        choices = {
            0: "rock",
            1: "paper",
            2: "scissors"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="Please choose", color=0xF59E42)
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xF59E42
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xE02B2B
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)
    
    @commands.command(name="8ball")
    async def magicball(self, ctx, *, arg=None):
        Answers=["Yes", "No","My sources say no", "Signs lead to no", "Without a doubt", "It is decidedly so", "Definitly", "Dont rely on it", "Outlook, not good", "As I see it, yes", "Very doubtful"]
        Answer=(random.choice(Answers))
        embed=discord.Embed(title="Magic Ball:8ball:", description="Ask the Magic 8 Ball anything\nand you will receive an answer!", color = 121314)
        embed.set_thumbnail(url="https://i.ibb.co/0QRZMBJ/st-small-507x507-pad-600x600-f8f8f8-u7.jpg")
        embed.add_field(name="Question", value=arg)
        embed.add_field(name="Answer", value=Answer)
        if arg == None:
            await ctx.send("You need to ask a question!")
        else:
            await ctx.send(embed=embed)

    @commands.command(name="fact")
    @commands.cooldown(1, 86400, BucketType.user)
    async def fact(self, context):
        """
        Get a daily fact, command can only be ran once every day per user.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                    await context.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)
                    # We need to reset the cool down since the user didn't got his daily fact.
                    self.dailyfact.reset_cooldown(context)

    @commands.command(name="bitcoin")
    async def bitcoin(self, context):
        """
        Get the current price of bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=0x42F56C
            )
            await context.send(embed=embed)

    @commands.command()
    async def roast(self, ctx):
        response = request.get(url="https://evilinsult.com/generate_insult.php?lang=en&type=json")
        roast = json.loads(response.text)
        await ctx.send(roast['insult'])
def setup(bot):
    bot.add_cog(Fun(bot))