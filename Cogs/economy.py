#Imports

from discord import user
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
            money_in_bank integer,
            items text
        )""")
        self.conn.commit()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items(
            name text,
            price integer,
            description text
        )""")
        self.conn.commit()

    @commands.command(aliases=["bal", "money", "account", "cash"])
    async def balance(self, ctx, *, user: discord.Member=None):
        if user is None:
            user_id = ctx.author.id
        else:
            user_id = int(user.id)
        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (int(user_id),))
        user_db = self.cursor.fetchone()
        if user_db:
            user = await self.bot.fetch_user(user_id)
            embed = discord.Embed(title=f"{user}", color=0x109414)
            embed.add_field(name="Money In Hand:", value=f":moneybag:{user_db[1]}", inline=False)
            embed.add_field(name="Money In Bank:", value=f":moneybag:{user_db[2]}", inline=False)
            await ctx.send(embed=embed)
        else:
            user = await self.bot.fetch_user(user_id)
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

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, *, amount="all"):
        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (ctx.author.id,))
        user_db = self.cursor.fetchone()

        if user_db:
            if amount == "all":
                hand = user_db[1]-user_db[1]
                bank = user_db[1]

                self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?, money_in_bank=?
                        WHERE user_id=?""", (hand, bank, ctx.author.id,))
                self.conn.commit()

                embed = discord.Embed(title=f"{ctx.author} deposited {bank} dollars!", color=0x109414)
                await ctx.send(embed=embed)
            else:
                bank = int(amount)

                if bank > user_db[1]:
                    embed = discord.Embed(title=f"You don't have that much money!", color=0xFF0000)
                    await ctx.send(embed=embed)
                    return

                hand = user_db[1]-bank
                
                self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?, money_in_bank=?
                        WHERE user_id=?""", (hand, bank, ctx.author.id,))
                self.conn.commit()

                embed = discord.Embed(title=f"{ctx.author} deposited {bank} dollars!", color=0x109414)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You don't have that much money!", color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=["wd"])
    async def withdraw(self, ctx, *, amount="all"):
        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (ctx.author.id,))
        user_db = self.cursor.fetchone()

        if user_db:
            if amount == "all":
                bank = user_db[2]-user_db[2]
                hand = user_db[2]

                self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?, money_in_bank=?
                        WHERE user_id=?""", (hand + user_db[1], bank, ctx.author.id,))
                self.conn.commit()

                embed = discord.Embed(title=f"{ctx.author} withdrew {hand} dollars!", color=0x109414)
                await ctx.send(embed=embed)
            else:
                hand = int(amount)

                if hand > user_db[2]:
                    embed = discord.Embed(title=f"You don't have that much money!", color=0xFF0000)
                    await ctx.send(embed=embed)
                    return

                bank = user_db[2]-hand
                
                self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?, money_in_bank=?
                        WHERE user_id=?""", (hand + user_db[1], bank, ctx.author.id,))
                self.conn.commit()

                embed = discord.Embed(title=f"{ctx.author} withdrew {hand} dollars!", color=0x109414)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You don't have that much money!", color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def give(self, ctx, user: discord.Member, amount):
        recipient_id = int(user.id)
        user_id = ctx.author.id
        amount = int(amount)

        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (recipient_id,))
        recipient_db = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (user_id,))
        user_db = self.cursor.fetchone()

        if user_db and recipient_db:
            hand = user_db[1]
            
            if hand < amount:
                embed = discord.Embed(title=f"You don't have that much money!", color=0xFF0000)
                await ctx.send(embed=embed)

            hand = hand - amount
            
            self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (hand, user_id,))
            self.conn.commit()

            self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (amount + recipient_db[1], recipient_id,))
            self.conn.commit()

            user = await self.bot.fetch_user(recipient_id)
            embed = discord.Embed(title=f"{ctx.author} gave {user} {amount} dollars!", color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            if not user_db and recipient_db:
                self.cursor.execute("""INSERT INTO bank VALUES (?, 0, 0)""",
                      (recipient_id,))
                self.conn.commit()

                self.cursor.execute("""INSERT INTO bank VALUES (?, 0, 0)""",
                      (user_id,))
                self.conn.commit()

                embed = discord.Embed(title=f"You don't have that much money!", color=0xFF0000)
                await ctx.send(embed=embed)

            elif not recipient_db:
                self.cursor.execute("""INSERT INTO bank VALUES (?, 0, 0)""",
                      (recipient_id,))
                self.conn.commit()

                self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (amount, recipient_id,))
                self.conn.commit()

                user = await self.bot.fetch_user(recipient_id)
                embed = discord.Embed(title=f"{ctx.author} gave {user} {amount} dollars!", color=0xFF0000)
                await ctx.send(embed=embed)

            elif not user_db:
                self.cursor.execute("""INSERT INTO bank VALUES (?, 0, 0)""",
                      (user_id,))
                self.conn.commit()

                embed = discord.Embed(title=f"You don't have that much money!", color=0xFF0000)
                await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (ctx.author.id,))
        user_db = self.cursor.fetchone()

        if user_db:
            earn = 500
            pay = user_db[1] + earn

            self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (pay, ctx.author.id,))
            self.conn.commit()

            embed = discord.Embed(title=f"{ctx.author} got their daily {earn} dollars!", color=0x109414)
            await ctx.send(embed=embed)
        else:
            self.cursor.execute("""INSERT INTO bank VALUES (?, 0, 0)""",
                      (ctx.author.id,))
            self.conn.commit()

            self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (ctx.author.id,))
            user_db = self.cursor.fetchone()

            earn = 500
            pay = user_db[1] + earn

            self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (pay, ctx.author.id,))
            self.conn.commit()

            embed = discord.Embed(title=f"{ctx.author} got their daily {earn} dollars!", color=0x109414)
            await ctx.send(embed=embed)

    @commands.command(aliases=["set"])
    @commands.has_permissions(manage_roles=True)
    async def set_(self, ctx, user: discord.Member, amount):
        user_id = int(user.id)

        self.cursor.execute("SELECT * FROM bank WHERE user_id=?", (user_id,))
        user_db = self.cursor.fetchall()

        if user_db:
            self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (int(amount) + user_db[1], user_id,))
            self.conn.commit()

            embed = discord.Embed(title=f"{ctx.author} gave {user} {amount} dollars!", color=0x109414)
            await ctx.send(embed=embed)
        else:
            self.cursor.execute("""INSERT INTO bank VALUES (?, 0, 0)""",
                      (ctx.author.id,))
            self.conn.commit()

            self.cursor.execute("""UPDATE bank
                        SET money_in_hand=?
                        WHERE user_id=?""", (int(amount), user_id,))
            self.conn.commit()

            embed = discord.Embed(title=f"{ctx.author} gave {user} {amount} dollars!", color=0x109414)
            await ctx.send(embed=embed)

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        self.cursor.execute("""SELECT * FROM bank ORDER BY money_in_hand DESC LIMIT 5""")
        top_user_db = self.cursor.fetchall()

        embed=discord.Embed(title="Leaderboard")

        for user_db in reversed(top_user_db):
            user = await self.bot.fetch_user(int(user_db[0]))
            embed.add_field(name=user, value=f"{user_db[2]} :moneybag:", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def shop(self, ctx):
        self.cursor.execute("""SELECT * FROM items LIMIT 10""")
        items = self.cursor.fetchall()

        embed=discord.Embed(title="Leaderboard")

        for item_db in items:
            embed.add_field(name=f"{item_db[0]} {item_db[1]} :moneybag:", value=item_db[2], inline=False)

        await ctx.send(embed=embed)

#Setup Cog

def setup(bot):
    bot.add_cog(Template(bot))
