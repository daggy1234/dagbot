"""
    Dagbot is a discord meme bot that does nothing useful
    Copyright (C) 2020  Daggy1234

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import random

import discord
import sr_api
from discord.ext import commands

client = sr_api.Client()


class animals(commands.Cog):
    """Animal facts and images"""

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if e["serverid"] == g_id:
                if e["animals"]:
                    return True
                else:
                    return False

    async def get_cat(self):
        response = await self.client.session.get("http://aws.random.cat/meow")
        file = await response.json()
        return file["file"]

    async def get_dog(self):
        response = await self.client.session.get("https://dog.ceo/api/breeds/image/random")
        file = await response.json()
        return file["message"]

    async def get_cat_fact(self):
        response = await self.client.session.get("https://cat-fact.herokuapp.com/facts")
        ict = await response.json()
        fileict = ict["all"]
        y = random.randint(0, len(fileict) - 1)
        return fileict[y]["text"]

    @commands.command(cooldown_after_parsing=True, aliases=["cat pic", "catp"])
    async def cat(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        link = await self.get_cat()
        embed = discord.Embed(
            title="DAGBOT -  Cat Pictures",
            color=guild.me.color
        )
        embed.set_image(url=link)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=["dog pic", "dogp"])
    async def dog(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        link = await self.get_dog()
        embed = discord.Embed(
            title="DAGBOT - Dog Pictures",
            color=guild.me.color
        )
        embed.set_image(url=link)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def panda(self, ctx):
        await ctx.trigger_typing()
        y = await client.get_image("panda")
        embed = discord.Embed(title="Cute Panda!", color=ctx.guild.me.color)
        embed.set_image(url=y.url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def fox(self, ctx):
        await ctx.trigger_typing()
        y = await client.get_image("fox")
        embed = discord.Embed(title="Cute Fox!", color=ctx.guild.me.color)
        embed.set_image(url=y.url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def racoon(self, ctx):
        await ctx.trigger_typing()
        y = await client.get_image("racoon")

        embed = discord.Embed(title="Cute Racoon!", color=ctx.guild.me.color)
        embed.set_image(url=y.url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=["bird"])
    async def birb(self, ctx):
        await ctx.trigger_typing()
        y = await client.get_image("birb")

        embed = discord.Embed(
            title="Cute Birb (bird)!",
            color=ctx.guild.me.color)
        embed.set_image(url=y.url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def racoon(self, ctx):
        await ctx.trigger_typing()
        y = await client.get_image("racoon")

        embed = discord.Embed(title="Cute Racoon!", color=ctx.guild.me.color)
        embed.set_image(url=y.url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def kangaroo(self, ctx):
        await ctx.trigger_typing()
        y = await client.get_image("racoon")

        embed = discord.Embed(title="Cute Kangaroo!", color=ctx.guild.me.color)
        embed.set_image(url=y.url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def koala(self, ctx):
        await ctx.trigger_typing()
        y = await client.get_image("koala")

        embed = discord.Embed(title="Cute Koala!", color=ctx.guild.me.color)
        embed.set_image(url=y.url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=["catf", "cf"])
    async def catfact(self, ctx):
        await ctx.trigger_typing()
        guild = ctx.guild
        cf = await self.get_cat_fact()
        embed = discord.Embed(title="DAGBOT - CAT FACT", color=guild.me.color)
        embed.add_field(name="fact", value=cf)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def dogfact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("dog")
        embed = discord.Embed(
            title="Dog Fact!",
            description=fact,
            color=guild.me.color)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def foxfact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("fox")
        embed = discord.Embed(
            title="Fox Fact!",
            description=fact,
            color=guild.me.color)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def koalafact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("koala")
        embed = discord.Embed(
            title="Koala Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def birdfact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("bird")
        embed = discord.Embed(
            title="Bird Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def elephantfact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("elephant")
        embed = discord.Embed(
            title="Elephant Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def pandafact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("panda")
        embed = discord.Embed(
            title="Panda Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def racoonfact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("racoon")
        embed = discord.Embed(
            title="Racoon Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def kangaroofact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("kangaroo")
        embed = discord.Embed(
            title="Kangaroo Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def whalefact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("whale")
        embed = discord.Embed(
            title="Whale Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    # giraffe
    @commands.command(cooldown_after_parsing=True)
    async def racoonfact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("racoon")
        embed = discord.Embed(
            title="Racoon Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def giraffefact(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        fact = await client.get_fact("giraffe")
        embed = discord.Embed(
            title="Giraffe Fact!", description=fact, color=guild.me.color
        )
        return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(animals(client))
