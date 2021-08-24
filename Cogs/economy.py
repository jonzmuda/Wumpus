#Imports

from discord.ext import commands
import discord
import os
from discord.ext.commands import bot
from dotenv import load_dotenv
import asyncio
import random
import json
import sqlite3

load_dotenv()

#Variables

Prefix = os.getenv("Prefix")
Name = os.getenv("Name")
Owners = os.getenv("Owners")

#Load Cog

class Template(commands.Cog, name="Template"):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bank(
            user_id integer,
            money_in_hand integer,
            money_in_bank integer
        )""")
        self.conn.commit()

    @commands.command(aliases=["bal", "money", "account", "cash"])
    async def balance(self, ctx, *, user: discord.Member=None):
        if user is None:
            user_id = ctx.author.id
        user_id = int(user.id)
        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (int(user_id),))
        user_db = self.cursor.fetchone()
        if user_db:
            embed = discord.Embed(title=f"{user}", color=0x109414)
            embed.add_field(name="Money In Hand:", value=f":moneybag:{user_db[1]}", inline=False)
            embed.add_field(name="Money In Bank:", value=f":moneybag:{user_db[2]}", inline=False)
            await ctx.send(embed=embed)
        else:
            self.cursor.execute("""INSERT INTO bank VALUES (?, 0, 0)""",
                      (user_id,))
            self.conn.commit()
            self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (int(user_id),))
            user_db = self.cursor.fetchone()
            embed = discord.Embed(title=f"{user}", color=0x109414)
            embed.add_field(name="Money In Hand:", value=f":moneybag:{user_db[1]}", inline=False)
            embed.add_field(name="Money In Bank:", value=f":moneybag:{user_db[2]}", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def work(self, ctx):
        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (ctx.author.id,))
        user_db = self.cursor.fetchone()

        if user_db:
            earn = random.randrange(100, 200)
            pay = user_db[1] + earn

            self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (pay, ctx.author.id,))
            self.conn.commit()

            embed = discord.Embed(title=f"{ctx.author} worked and earned {earn} dollars!", color=0x109414)
            await ctx.send(embed=embed)
        else:
            self.cursor.execute("""INSERT INTO bank VALUES (?, 0, 0)""",
                      (ctx.author.id,))
            self.conn.commit()

            self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (ctx.author.id,))
            user_db = self.cursor.fetchone()

            earn = random.randrange(100, 200)
            pay = user_db[1] + earn

            self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (pay, ctx.author.id,))
            self.conn.commit()

            embed = discord.Embed(title=f"{ctx.author} worked and earned {earn} dollars!", color=0x109414)
            await ctx.send(embed=embed)


#Setup Cog

def setup(bot):
    bot.add_cog(Template(bot))