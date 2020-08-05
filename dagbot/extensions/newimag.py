import os
import random
import shutil
import typing
from functools import partial
from io import BytesIO

import aiohttp
import discord
import PIL
import sr_api
from discord.ext import commands
from PIL import (Image, ImageDraw, ImageEnhance, ImageFont, ImageOps,
                 ImageSequence)
from utils.converters import BetterMemberConverter, ImageConverter

client = sr_api.Client()
# atMoMn2Pg3EUmZ065QBvdJN4IcjNxCQRMv1oZTZWg98i7HelIdvJwHtZFKPgCtf


def setup(client):
    client.add_cog(image(client))


class image(commands.Cog):
    """Funny images produced by me!"""

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        print("start")
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                if e["image"]:
                    return True
                else:
                    return False

    @commands.command(cooldown_after_parsing=True)
    async def gay(self, ctx, *, source=None):

        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("jail", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def triggered(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("triggered", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def tweet(self, ctx, user=None, *, text):
        if user is None:
            user = ctx.author
        user = await BetterMemberConverter().convert(ctx, user)
        uname = user.display_name
        text = str(text)
        pfp = str(user.avatar_url_as(format="png", size=1024))
        y = await self.client.dagpi.usertextimage("tweet", pfp, text, uname)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def spin(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)

        f = await client.beta("spin", image_url)
        async with aiohttp.ClientSession() as session:
            async with session.get(f) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(file=discord.File(bio, filename="spin.gif")))

    @commands.command(cooldown_after_parsing=True)
    async def wanted(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("wanted", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)
    @commands.command(cooldown_after_parsing=True)
    async def asciiimage(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("ascii", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)
    @commands.command(cooldown_after_parsing=True)
    async def sobel(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("sobel", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)
    @commands.command(cooldown_after_parsing=True)
    async def hog(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("hog", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)
    @commands.command(cooldown_after_parsing=True)
    async def colors(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("colors", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)
    @commands.command(cooldown_after_parsing=True)
    async def evil(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("evil", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def deepfry(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("deepfry", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

   

    @commands.command(cooldown_after_parsing=True)
    async def invert(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("invert", image_url)
        if isinstance(y, str):
            return await ctx.send(y)
        else:
            io = BytesIO(y)
            io.seek(0)
            await (ctx.send(file=discord.File(io, filename="invert.gif")))

    @commands.command(cooldown_after_parsing=True)
    async def blur(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("blur", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def wasted(
        self, ctx, *, source=None
    ):

        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("wasted", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def hitler(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("hitler", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=["8bit", "retro"])
    async def pixel(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("pixel", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def thoughtimage(
        self,
        ctx,
        source: typing.Union[discord.Member, str],
        *,
        text: str = "I was too dumb to add text",
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.bot.dagpi.textimage("thoughtimage", image_url, text)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def trash(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("trash", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def angel(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("angel", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def satan(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.staticimage("satan", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=['av', 'pfp'])
    async def avatar(self, ctx, *, user=None):
        await ctx.trigger_typing()
        if user is None:
            user = ctx.author
        user = await BetterMemberConverter().convert(ctx, user)
        url = user.avatar_url
        guy = user.display_name
        embed = discord.Embed(
            title=f"{guy}'s Profile Pic",
            color=ctx.guild.me.color)
        embed.set_image(url=url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def salty(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        url = f"https://api.alexflipnote.dev/salty?image={image_url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(file=discord.File(bio, filename="salty.png")))

    @commands.command(cooldown_after_parsing=True)
    async def achievement(self, ctx, *, text):
        await ctx.trigger_typing()
        inta = random.randint(1, 44)
        url = f"https://api.alexflipnote.dev/achievement?text={text}&icon={inta}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(file=discord.File(bio, filename="achieve.png")))

    @commands.command(cooldown_after_parsing=True)
    async def challenge(self, ctx, *, text):
        await ctx.trigger_typing()
        inta = random.randint(1, 44)
        url = f"https://api.alexflipnote.dev/challenge?text={text}&icon={inta}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(file=discord.File(bio, filename="chal.png")))

    @commands.command(cooldown_after_parsing=True)
    async def didyoumean(
        self,
        ctx,
        *,
        text="I forgot to add text,split with a comma to indicate top and bottom text",
    ):
        await ctx.trigger_typing()
        txtl = text.split(",")
        try:
            ttop = txtl[0]
            tbot = txtl[1]
        except BaseException:
            return await ctx.send("Please use a comma to split top and bottom text")
        else:
            url = f"https://api.alexflipnote.dev/didyoumean?top={ttop}&bottom={tbot}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as y:
                    z = y.content
                    file = await z.read()
                    bio = BytesIO(file)
                    bio.seek(0)
                    await (ctx.send(file=discord.File(bio, filename="dym.png")))

    @commands.command(cooldown_after_parsing=True)
    async def paint(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("paint", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def sepia(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("sepia", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def charcoal(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        y = await self.client.dagpi.gif("charcoal", image_url)
        if isinstance(y, str):
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=y)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def pornhub(
        self,
        ctx,
        *,
        text="I forgot to add text,split with a comma for white and orange",
    ):
        await ctx.trigger_typing()
        txtl = text.split(",")
        try:
            ttop = txtl[0]
            tbot = txtl[1]
        except BaseException:
            return await ctx.send("Please use a comma to split your white and orange  text")
        else:
            url = f"https://api.alexflipnote.dev/pornhub?text={ttop}&text2={tbot}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as y:
                    z = y.content
                    file = await z.read()
                    bio = BytesIO(file)
                    bio.seek(0)
                    await (ctx.send(file=discord.File(bio, filename="phub.png")))

    @commands.command(cooldown_after_parsing=True)
    async def bad(self, ctx, *, source=None):
        image_url = await ImageConverter().convert(ctx, source)
        url = f"https://api.alexflipnote.dev/bad?image={image_url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(file=discord.File(bio, filename="bad.png")))

    @commands.command(cooldown_after_parsing=True)
    async def ship(self, ctx, user: discord.Member, usert: discord.Member):
        await ctx.trigger_typing()
        urla = str(user.avatar_url_as(format="png", size=1024))
        guya = user.display_name
        urlb = str(usert.avatar_url_as(format="png", size=1024))
        guyb = usert.display_name
        if guya == guyb:
            return await ctx.send("Thats just loving yourself.")
        else:
            url = f"https://api.alexflipnote.dev//ship?user={urla}&user2={urlb}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as y:
                    z = y.content
                    file = await z.read()
                    bio = BytesIO(file)
                    bio.seek(0)
                    await (ctx.send(file=discord.File(bio, filename="ship.png")))

    @commands.command(cooldown_after_parsing=True, aliases=["jokeoverhead"])
    async def woosh(
        self, ctx, *, source=None
    ):
        image_url = await ImageConverter().convert(ctx, source)
        url = f"https://api.alexflipnote.dev/jokeoverhead?image={image_url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(file=discord.File(bio, filename="jokeoverhead.png")))

    @commands.command(cooldown_after_parsing=True)
    async def amiajoke(self, ctx, user: discord.Member = None):
        await ctx.trigger_typing()
        if user is None:
            guy = ctx.author
            urlp = str(guy.avatar_url_as(format="png", size=1024))
        else:
            try:
                urlp = str(user.avatar_url_as(format="png", size=1024))
            except BaseException:
                guy = ctx.author
                urlp = str(guy.avatar_url_as(format="png", size=1024))
        url = f"https://api.alexflipnote.dev//amiajoke?image={urlp}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(file=discord.File(bio, filename="amiajoke.png")))
