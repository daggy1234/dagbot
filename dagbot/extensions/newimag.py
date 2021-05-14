import random
import time
import typing
from datetime import datetime
from io import BytesIO

import asyncdagpi
import discord
from asyncdagpi import ImageFeatures, Image
from discord.ext import commands

from dagbot.utils.exceptions import NoImageFound
from ..utils.converters import BetterMemberConverter, ImageConverter, \
    StaticImageConverter


# atMoMn2Pg3EUmZ065QBvdJN4IcjNxCQRMv1oZTZWg98i7HelIdvJwHtZFKPgCtf


def setup(client):
    client.add_cog(image(client))


class image(commands.Cog):
    """Funny images produced by me!"""

    def __init__(self, client):
        self.client = client
        self.dynamic = [
            (ImageFeatures.night(),
             ImageConverter),
            (ImageFeatures.gay(),
             ImageConverter),
            (ImageFeatures.wanted(),
             ImageConverter),
            (ImageFeatures.ascii(),
             StaticImageConverter),
            (ImageFeatures.sobel(),
             StaticImageConverter),
            (ImageFeatures.hog(),
             StaticImageConverter),
            (ImageFeatures.colors(),
             StaticImageConverter),
            (ImageFeatures.rgb(),
             StaticImageConverter),
            (ImageFeatures.sith(),
             StaticImageConverter),
            (ImageFeatures.triggered(),
             StaticImageConverter),
            (ImageFeatures.deepfry(),
             ImageConverter),
            (ImageFeatures.invert(),
             ImageConverter),
            (ImageFeatures.wasted(),
             ImageConverter),
            (ImageFeatures.communism(),
             StaticImageConverter),
            (ImageFeatures.america(),
             StaticImageConverter),
            (ImageFeatures.pixel(),
             ImageConverter),
            (ImageFeatures.fedora(),
             ImageConverter),
            (ImageFeatures.jail(),
             ImageConverter),
            (ImageFeatures.magik(),
             StaticImageConverter),
            (ImageFeatures.rainbow(),
             ImageConverter),
            (ImageFeatures.triangle(),
             StaticImageConverter),
            (ImageFeatures.stringify(), StaticImageConverter),
            (ImageFeatures.neon(), StaticImageConverter),
            (ImageFeatures.sketch(), StaticImageConverter),
            (ImageFeatures.dissolve(), StaticImageConverter),
            (ImageFeatures.bonk(), StaticImageConverter),
            (ImageFeatures.petpet(), StaticImageConverter)

        ]
        for command in self.dynamic:
            self.make_fn(command[0], command[1])
        self.make_fn_alex("salty", StaticImageConverter)
        self.make_fn_alex("jokeoverhead", StaticImageConverter)

    def make_fn(self, feature: asyncdagpi.ImageFeatures,
                converter: typing.Union
                [ImageConverter, StaticImageConverter]):
        @commands.command(name=feature.value.replace("/", ""),
                          help=feature.description)
        async def _command(_self, ctx, *, source: converter = None):
            if source is None:
                raise NoImageFound('Please provide a valid image')
            img = await self.client.dagpi.image_process(feature,
                                                        source)

            await self.to_embed(ctx, img, feature.value.replace("/", ""))

        _command.cog = self
        self.__cog_commands__ += (_command,)

    async def process_alex(self, url: str) -> BytesIO:
        out = await self.client.session.get(url, headers={
            "Authorization": self.client.data["alex"]})
        return BytesIO(await out.read())

    def make_fn_alex(self, feature: str, converter: typing.Union
    [ImageConverter, StaticImageConverter]):
        @commands.command(name=feature)
        async def _command(_self, ctx, *, source: converter):
            start = time.perf_counter()
            url = f"https://api.alexflipnote.dev/{feature}?image={source}"
            img = await self.process_alex(url)
            end = time.perf_counter()
            await self.to_embed_alex(ctx, img, end - start, feature)

        _command.cog = self
        self.__cog_commands__ += (_command,)

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                return bool(e["image"])

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
            await ctx.reply(embed=embed, file=file)

    async def to_embed_alex(self, ctx, img: BytesIO,
                            time: typing.Optional[float], feature: str):
        async with ctx.typing():
            embed = discord.Embed(color=ctx.guild.me.color)
            filename = f"dagbot=process-image-{feature}.png"
            file = discord.File(fp=img, filename=filename)
            if time:
                embed.description = f"Image Processed in {round(time, 2)}s | " \
                                    f"Powered by [AlexFlipnote](https://api.alexflipnote.dev/)"
            else:
                embed.description = "Powered by [AlexFlipnote](https://api.alexflipnote.dev/)"
            embed.timestamp = datetime.utcnow()
            embed.title = f"Processed Image {feature}"
            embed.set_footer(icon_url=str(ctx.author.avatar_url),
                             text=f"Called by {ctx.author.display_name}")
            await ctx.reply(embed=embed, file=file)

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
    async def captcha(self, ctx, user: BetterMemberConverter = None, *,
                      text: str):
        if user is None:
            user = ctx.author
        pfp = str(user.avatar_url_as(format="png", size=1024))
        img = await self.client.dagpi.image_process(ImageFeatures.captcha(),
                                                    url=pfp,
                                                    text=text)
        await self.to_embed(ctx, img, "captcha")

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
    async def comment(self, ctx, user: BetterMemberConverter = None, *, text):
        if user is None:
            user = ctx.author
        uname = user.display_name
        text = str(text)
        pfp = str(user.avatar_url_as(format="png", size=1024))
        img = await self.client.dagpi.image_process(ImageFeatures.youtube(),
                                                    url=pfp,
                                                    username=uname,
                                                    text=text)
        await self.to_embed(ctx, img, "comment")

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
    async def achievement(self, ctx, *, text):
        url = f"https://api.alexflipnote.dev/achievement?text={text}&icon={random.randint(1, 44)}"
        await self.to_embed_alex(ctx, await self.process_alex(url), None,
                                 "achievement")

    @commands.command(cooldown_after_parsing=True)
    async def challenge(self, ctx, *, text):
        url = f"https://api.alexflipnote.dev/challenge?text={text}&icon={random.randint(1, 44)}"
        await self.to_embed_alex(ctx, await self.process_alex(url), None,
                                 "challenge")

    @commands.command(cooldown_after_parsing=True)
    async def didyoumean(
            self,
            ctx,
            *,
            text=None,
    ):
        txtl = str(text).split(
            ",") if text else "Oops I forgot to add text, Seperated by a comma"
        try:
            ttop = txtl[0]
            tbot = txtl[1]
        except IndexError:
            return await ctx.send(
                "Please use a comma to split top and bottom text")

        url = f"https://api.alexflipnote.dev/didyoumean?top={ttop}" \
              f"&bottom={tbot}"
        await self.to_embed_alex(ctx, await self.process_alex(url), None,
                                 "didyoumean")

    @commands.command(cooldown_after_parsing=True)
    async def pornhub(
            self,
            ctx,
            *,
            text=None
    ):
        txtl = str(text).split(
            ",") if text else "Oops I forgot to add text, Seperated by comma"
        try:
            ttop = txtl[0]
            tbot = txtl[1]
        except IndexError:
            return await ctx.send(
                "Please use a comma to split top and bottom text")

        url = f"https://api.alexflipnote.dev/pornhub?top={ttop}" \
              f"&bottom={tbot}"
        await self.to_embed_alex(ctx, await self.process_alex(url), None,
                                 "pornhub")

    @commands.command(cooldown_after_parsing=True)
    async def ship(self, ctx, user: BetterMemberConverter,
                   usert: BetterMemberConverter):
        urla = str(user.avatar_url_as(format="png", size=1024))
        guya = user.display_name
        urlb = str(usert.avatar_url_as(format="png", size=1024))
        guyb = usert.display_name
        if guya == guyb:
            return await ctx.send("Thats just loving yourself.")
        url = f"https://api.alexflipnote.dev//ship?user={urla}" \
              f"&user2={urlb}"
        await self.to_embed_alex(ctx, await self.process_alex(url), None,
                                 "ship")
