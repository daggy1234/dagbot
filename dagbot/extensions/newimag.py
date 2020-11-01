import random
from datetime import datetime
from io import BytesIO

import aiohttp
import discord
from asyncdagpi import ImageFeatures, Image
from discord.ext import commands

from ..utils.converters import BetterMemberConverter, ImageConverter


# atMoMn2Pg3EUmZ065QBvdJN4IcjNxCQRMv1oZTZWg98i7HelIdvJwHtZFKPgCtf


def setup(client):
    client.add_cog(image(client))


class image(commands.Cog):
    """Funny images produced by me!"""

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                if e["image"]:
                    return True
                else:
                    return False

    async def to_embed(self, ctx, img: Image, feature: str):
        async with ctx.typing():
            io = img.image
            embed = discord.Embed(color=ctx.guild.me.color)
            filename = f"dagbot=process-image-{feature}.{img.format}"
            file = discord.File(fp=io, filename=filename)
            embed.description = f"Image Processed in {img.process_time}s | " \
                                f"Powered by [dagpi](https://dagpi.xyz)"
            embed.timestamp = datetime.utcnow()
            embed.title = f"Processed Image {feature}"
            embed.set_footer(icon_url=str(ctx.author.avatar_url),
                             text=f"Called by {ctx.author.display_name}")
            await ctx.send(embed=embed, file=file)

    @commands.command(cooldown_after_parsing=True)
    async def gay(self, ctx, *, source: ImageConverter):
        img = await self.client.dagpi.image_process(ImageFeatures.gay(),
                                                    source)
        await self.to_embed(ctx, img, "gay")

    @commands.command(cooldown_after_parsing=True)
    async def triggered(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.triggered(),
                                                    source)
        await self.to_embed(ctx, img, "triggered")

    @commands.command(cooldown_after_parsing=True)
    async def tweet(self, ctx, user: BetterMemberConverter = None, *, text):
        if user is None:
            user = ctx.author
        uname = user.display_name
        text = str(text)
        pfp = str(user.avatar_url_as(format="png", size=1024))
        img = await self.client.dagpi.image_process(ImageFeatures.tweet(),
                                                    url=pfp,
                                                    username=uname,
                                                    text=text)
        await self.to_embed(ctx, img, "tweet")

    @commands.command(cooldown_after_parsing=True)
    async def message(self, ctx, user: BetterMemberConverter = None, *, text):
        if user is None:
            user = ctx.author
        uname = user.display_name
        text = str(text)
        pfp = str(user.avatar_url_as(format="png", size=1024))
        img = await self.client.dagpi.image_process(ImageFeatures.discord(),
                                                    url=pfp,
                                                    username=uname,
                                                    text=text)
        await self.to_embed(ctx, img, "message")

    @commands.command(cooldown_after_parsing=True)
    async def wanted(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.wanted(),
                                                    source)
        await self.to_embed(ctx, img, "wanted")

    @commands.command(cooldown_after_parsing=True)
    async def asciiimage(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.ascii(),
                                                    source)
        await self.to_embed(ctx, img, "ascii")

    @commands.command(cooldown_after_parsing=True)
    async def sobel(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.sobel(),
                                                    source)
        await self.to_embed(ctx, img, "sobel")

    @commands.command(cooldown_after_parsing=True)
    async def hog(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.hog(),
                                                    source)
        await self.to_embed(ctx, img, "hog")

    @commands.command(cooldown_after_parsing=True)
    async def colors(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.colors(),
                                                    source)
        await self.to_embed(ctx, img, "colors")

    @commands.command(cooldown_after_parsing=True)
    async def evil(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.sith(),
                                                    source)
        await self.to_embed(ctx, img, "evil")

    @commands.command(cooldown_after_parsing=True)
    async def deepfry(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.deepfry(),
                                                    source)
        await self.to_embed(ctx, img, "deepfry")

    @commands.command(cooldown_after_parsing=True)
    async def invert(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.invert(),
                                                    source)
        await self.to_embed(ctx, img, "invert")

    @commands.command(cooldown_after_parsing=True)
    async def blur(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.blur(),
                                                    source)
        await self.to_embed(ctx, img, "blur")

    @commands.command(cooldown_after_parsing=True)
    async def wasted(
            self, ctx, *, source: ImageConverter
    ):

        img = await self.client.dagpi.image_process(ImageFeatures.wasted(),
                                                    source)
        await self.to_embed(ctx, img, "wasted")

    @commands.command(cooldown_after_parsing=True)
    async def hitler(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.hitler(),
                                                    source)
        await self.to_embed(ctx, img, "hitler")

    @commands.command(cooldown_after_parsing=True, aliases=["8bit", "retro"])
    async def pixel(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.pixel(),
                                                    source)
        await self.to_embed(ctx, img, "pixel")

    @commands.command(cooldown_after_parsing=True)
    async def thoughtimage(
            self,
            ctx,
            source: ImageConverter,
            *,
            text: str = "I was too dumb to add text",
    ):
        img = await self.client.dagpi.image_process(
            ImageFeatures.thought_image(),
            url=source, text=text
        )
        await self.to_embed(ctx, img, "thought image")

    @commands.command
    async def trash(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.trash(),
                                                    source)
        await self.to_embed(ctx, img, "trash")

    @commands.command(cooldown_after_parsing=True)
    async def angel(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.angel(),
                                                    source)
        await self.to_embed(ctx, img, "angel")

    @commands.command(cooldown_after_parsing=True)
    async def satan(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.satan(),
                                                    source)
        await self.to_embed(ctx, img, "satan")

    @commands.command(cooldown_after_parsing=True, aliases=['av', 'pfp'])
    async def avatar(self, ctx, *, user=None):
        await ctx.trigger_typing()
        if user is None:
            user = ctx.author
        else:
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
            self, ctx, *, source: ImageConverter
    ):
        url = f"https://api.alexflipnote.dev/salty?image={source}"
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
        url = f"https://api.alexflipnote.dev/achievement?\
            text={text}&icon={inta}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (
                    ctx.send(file=discord.File(bio, filename="achieve.png")))

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
            text="I forgot to add text,split with a comma to indicate top \
                and bottom text",
    ):
        await ctx.trigger_typing()
        txtl = text.split(",")
        try:
            ttop = txtl[0]
            tbot = txtl[1]
        except BaseException:
            return await ctx.send(
                "Please use a comma to split top and bottom text")
        else:
            url = f"https://api.alexflipnote.dev/didyoumean?top={ttop}" \
                  f"&bottom={tbot}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as y:
                    z = y.content
                    file = await z.read()
                    bio = BytesIO(file)
                    bio.seek(0)
                    await (
                        ctx.send(file=discord.File(bio, filename="dym.png")))

    @commands.command(cooldown_after_parsing=True)
    async def paint(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.paint(),
                                                    source)
        await self.to_embed(ctx, img, "paint")

    @commands.command(cooldown_after_parsing=True)
    async def sepia(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.sepia(),
                                                    source)
        await self.to_embed(ctx, img, "sepia")

    @commands.command(cooldown_after_parsing=True)
    async def charcoal(
            self, ctx, *, source: ImageConverter
    ):
        img = await self.client.dagpi.image_process(ImageFeatures.charcoal(),
                                                    source)
        await self.to_embed(ctx, img, "charcoal")

    @commands.command(cooldown_after_parsing=True)
    async def pornhub(
            self,
            ctx,
            *,
            text="I forgot to add text,split with a comma for white and orange"
    ):
        await ctx.trigger_typing()
        txtl = text.split(",")
        try:
            ttop = txtl[0]
            tbot = txtl[1]
        except BaseException:
            return await ctx.send(
                "Please use a comma to split your white and orange  text")
        else:
            url = f"https://api.alexflipnote.dev/pornhub?text={ttop}" \
                  f"&text2={tbot}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as y:
                    z = y.content
                    file = await z.read()
                    bio = BytesIO(file)
                    bio.seek(0)
                    await (
                        ctx.send(file=discord.File(bio, filename="phub.png")))

    @commands.command(cooldown_after_parsing=True)
    async def bad(self, ctx, *, source: ImageConverter):
        url = f"https://api.alexflipnote.dev/bad?image={source}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(file=discord.File(bio, filename="bad.png")))

    @commands.command(cooldown_after_parsing=True)
    async def ship(self, ctx, user: BetterMemberConverter,
                   usert: BetterMemberConverter):
        await ctx.trigger_typing()
        urla = str(user.avatar_url_as(format="png", size=1024))
        guya = user.display_name
        urlb = str(usert.avatar_url_as(format="png", size=1024))
        guyb = usert.display_name
        if guya == guyb:
            return await ctx.send("Thats just loving yourself.")
        else:
            url = f"https://api.alexflipnote.dev//ship?user={urla}" \
                  f"&user2={urlb}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as y:
                    z = y.content
                    file = await z.read()
                    bio = BytesIO(file)
                    bio.seek(0)
                    await (
                        ctx.send(file=discord.File(bio, filename="ship.png")))

    @commands.command(cooldown_after_parsing=True, aliases=["jokeoverhead"])
    async def woosh(
            self, ctx, *, source: ImageConverter
    ):
        url = f"https://api.alexflipnote.dev/jokeoverhead?image={source}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as y:
                z = y.content
                file = await z.read()
                bio = BytesIO(file)
                bio.seek(0)
                await (ctx.send(
                    file=discord.File(bio, filename="jokeoverhead.png")))
