import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
Prefix = os.getenv("Prefix")

class Help(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="format")
    async def format(self, ctx):
        embed = discord.Embed(title="Learn How To Format Text!", description="Quickly learn how to send code through discord!")
        embed.add_field(name="Sending Code!", value="'''py\n#Code Here```")
        embed.add_field(name="Outcome", value="```#Code Here```", inline=False)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Help(bot))