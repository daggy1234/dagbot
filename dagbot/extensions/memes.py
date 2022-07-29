import asyncio
from dagbot.bot import Dagbot
from dagbot.utils.context import MyContext
import json
from io import BytesIO
from typing import Dict, List, Optional

import discord
from asyncdagpi import ImageFeatures
from dagbot.extensions.newimag import image
from discord.ext import commands, menus

from dagbot.utils.converters import BetterMemberConverter, UrlValidator


async def setup(client: Dagbot):
    await client.add_cog(memes(client))





class Test:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value





class Source(menus.GroupByPageSource):
    async def format_page(self, menu, entry):
        offset = ((menu.current_page) * 10) + 1
        embed = discord.Embed(
            title=f"**{entry.key}**\tPage \
                {menu.current_page + 1}/{self.get_max_pages()}"
        )
        joined = "\n".join(
            f"{i}.{v.value}" for i, v in enumerate(entry.items, start=offset)
        )
        embed.description = (
                "Dagbot's meme generation tool allows you to "
                "access more than a 100+ meme templates.Browse through the "
                "meme templates using the buttons below!\n "
                "Once you select the template use the following template. "
                "Use semicolons to seperate the number of text arguments "
                "required! DO NOT NEED TO include all of them "
                "`create template:text1:text2`\n **For example**\n`create "
                "The scroll of truth:Dagbot is not the best:`\n"
                + joined
        )
        return embed


class memes(commands.Cog):
    """Helps you craft wonderful memes worth sharing"""

    def __init__(self, client: Dagbot):
        self.client: Dagbot = client
        topasslist: List[str] = []
        with open("./dagbot/data/imgfliptemplates.json", "r") as file:
            f = json.load(file)
            li = f["data"]["memes"]
            for e in li:
                elstring = f"[{e['name']}]({e['url']}): {e['box_count']} text boxes"
                topasslist.append(elstring)
        self.data = [Test(key=key, value=value) for key in [
            "Dagbot's meme generator"] for value in topasslist]
        cog: Optional[image] = self.client.get_cog("image")
        if not cog:
            raise Exception("No Imaging Cog")
        self.img_cog = cog

    async def getgeneratedmeme(self, data: Dict[str, str]):
        url = "https://api.imgflip.com/caption_image"
        r = await self.client.session.post(url, params=data)
        js = await r.json()
        return js

    async def cog_check(self, ctx: MyContext):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                return bool(e["memes"])

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(3, commands.BucketType.channel)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def create(self, ctx: MyContext, *, query: str = "none"):
        await ctx.typing()
        if query in ["none", "help"]:
            pages = menus.MenuPages(
                source=Source(self.data, key=lambda t: t.key, per_page=10),
                clear_reactions_after=True,
            )
            await pages.start(ctx)
        else:
            st = query.split(":")
            tosearch = st[0].lower()
            with open("./dagbot/data/imgfliptemplates.json") as file:
                f = json.load(file)
                li = f["data"]["memes"]
                timplist = [e["id"] for e in li if
                            tosearch in e["name"].lower()]
                if not timplist:
                    return await ctx.send(
                        "No results\nUse the command `create` to view the "
                        "options!"
                    )
                elif len(timplist) > 1:
                    return await ctx.send(
                        "More than 1 result please be specific to the query! "
                        "Use the command `create` to view the options!"
                    )
                else:
                    mastdict = {
                        "template_id": timplist[0],
                        "username": self.client.data['imgflipuser'],
                        "password": self.client.data['imgflippass'],
                    }
                    for i in range(1, len(st)):
                        dic = {
                            f"boxes[{i - 1}][type]": "text",
                            f"boxes[{i - 1}][text]": st[i],
                            f"boxes[{i - 1}][force_caps]": 0,
                        }
                        mastdict.update(dic)
                    if "text" not in str(mastdict):
                        return await ctx.send("No text was specified")
                    me = await self.getgeneratedmeme(mastdict)
                    if not me["success"]:
                        return await ctx.send(
                            f"Error Occurred! If this bug does not make "
                            f"sense please report it using the bug "
                            f"command!\nError:`{me['error_message']}`"
                        )

                    embed = discord.Embed(color=ctx.guild.me.color)
                    embed.set_image(url=me["data"]["url"])
                    embed.set_footer(
                        text=f"Rendered by {ctx.author.display_name}",
                        icon_url=ctx.author.avatar.url,
                    )
                    return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def motiv(self, ctx: MyContext):
        await ctx.typing()
        await ctx.send(
            "Lets begin. Please send an image. "
            "It can be a url or an attachment or a mention of a member!"
        )

        def check(message):
            return (
                    message.author == ctx.author
                    and message.channel == ctx.channel
                    and not message.author.bot
            )

        try:
            msg: discord.Message = await self.client.wait_for("message", timeout=60.0,
                                             check=check)
        except asyncio.TimeoutError:
            return await ctx.send(
                "No Image was provided, "
                "If you want me to make your meme at least give me "
                "something to work with"
            )
        else:
            try:
                cont = msg.content
                member = await BetterMemberConverter().convert(ctx, cont)
                image_url = str(member.avatar.with_static_format("png").with_size(1024))
            except Exception:
                pass
            if len(msg.attachments) != 0:
                try:
                    image_url = msg.attachments[0].url

                except KeyError or AttributeError:
                    return await ctx.send(
                        "I was unable to use the attachment you provided"
                    )
            elif len(msg.mentions) != 0:
                image_url = str(
                    msg.mentions[0].avatar.with_format("png").with_size(1024))
            else:
                source = msg.content
                val_stat = await UrlValidator().validate(source)
                if val_stat:
                    image_url = str(source)
                else:
                    return await ctx.send('The URL provided was invalid.')
            # byt = await self.getav(image_url)

            await ctx.send(
                "Great, now hit me we with the top_text for the meme. "
                "Please note whatever message you send is the content cool?"
            )
            try:
                tm = await self.client.wait_for(
                    "message", timeout=60.0, check=check
                )
            except asyncio.TimeoutError:
                return await ctx.send(
                    "No top text was provided, If you want me to make your "
                    "meme at least give me something to work with"
                )
            else:
                toptext = tm.content
            await ctx.send(
                "Great, now hit me we with the bottom_text for the meme. "
                "Please not whatever message you send is the content cul"
            )
            try:
                bm = await self.client.wait_for(
                    "message", timeout=60.0, check=check
                )
            except asyncio.TimeoutError:
                return await ctx.send(
                    "No top text was provided, If you want me to make your "
                    "meme at least give me something to work with"
                )
            else:
                bottomtext = bm.content
            await ctx.typing()
            img = await self.client.dagpi.image_process(
                ImageFeatures.motiv(), url=image_url, top_text=toptext,
                bottom_text=bottomtext)
            
            await self.img_cog.to_embed(ctx, img, "Retromeme")

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def retromeme(self, ctx: MyContext):
        await ctx.typing()
        await ctx.send(
            "Lets begin. Please send an image. "
            "It can be a url or an attachment or a mention of a member!"
        )

        def check(message):
            return (
                    message.author == ctx.author
                    and message.channel == ctx.channel
                    and not message.author.bot
            )

        try:
            msg: discord.Message = await self.client.wait_for("message", timeout=60.0,
                                             check=check)
        except asyncio.TimeoutError:
            return await ctx.reply(
                "No Image was provided, "
                "If you want me to make your meme at least give me "
                "something to work with"
            )
        else:
            try:
                cont = msg.content
                member = await BetterMemberConverter().convert(ctx, cont)
                image_url = str(member.avatar.with_static_format("png").with_size(1024))
            except Exception:
                pass
            if len(msg.attachments) != 0:
                try:
                    image_url = msg.attachments[0].url

                except KeyError or AttributeError:
                    return await msg.reply(
                        "I was unable to use the attachment you provided"
                    )
            elif len(msg.mentions) != 0:
                image_url = str(
                    msg.mentions[0].avatar.with_format("png").with_size(1024))
            else:
                source = msg.content
                val_stat = await UrlValidator().validate(source)
                if val_stat:
                    image_url = str(source)
                else:
                    return await msg.reply('The URL provided was invalid.')
            # byt = await self.getav(image_url)

            await msg.reply(
                "Great, now hit me we with the top_text for the meme. "
                "Please note whatever message you send is the content cool?"
            )
            try:
                tm = await self.client.wait_for(
                    "message", timeout=60.0, check=check
                )
            except asyncio.TimeoutError:
                return await msg.reply(
                    "No top text was provided, If you want me to make your "
                    "meme at least give me something to work with"
                )
            else:
                toptext = tm.content
            await ctx.send(
                "Great, now hit me we with the bottom_text for the meme. "
                "Please not whatever message you send is the content cul"
            )
            try:
                bm = await self.client.wait_for(
                    "message", timeout=60.0, check=check
                )
            except asyncio.TimeoutError:
                return await msg.reply(
                    "No top text was provided, If you want me to make your "
                    "meme at least give me something to work with"
                )
            else:
                bottomtext = bm.content
            await ctx.typing()
            img = await self.client.dagpi.image_process(
                ImageFeatures.retro_meme(), url=image_url, top_text=toptext,
                bottom_text=bottomtext)
            await self.img_cog.to_embed(ctx, img, "Retromeme")

    @commands.command(cooldown_after_parsing=True)
    async def drake(
            self,
            ctx: MyContext,
            *,
            text="I forgot to add text,split with a comma to "
                 "indicate top and bottom text",
    ):
        txtl = text.split(",")
        try:
            ttop = txtl[0]
            tbot = txtl[1]
        except BaseException:
            return await ctx.send(
                "Please use a comma to split your text into top and bottom")
        else:
            url = f"https://api.alexflipnote.dev/drake?top={ttop}&" \
                  f"bottom={tbot}"
            y = await self.client.session.get(url)
            z = y.content
            file = await z.read()
            bio = BytesIO(file)
            bio.seek(0)
            await (ctx.send(file=discord.File(bio, filename="drake.png")))

    @commands.command(cooldown_after_parsing=True, aliases=['mm'])
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def modernmeme(self, ctx: MyContext):
        await ctx.typing()
        await ctx.send(
            "Lets begin. Please send an image. It can be a url or an "
            "attachment or a mention of a member!"
        )

        def check(message):
            return (
                    message.author == ctx.author
                    and message.channel == ctx.channel
                    and not message.author.bot
            )

        try:
            msg: discord.Message = await self.client.wait_for("message", timeout=60.0,
                                             check=check)
        except asyncio.TimeoutError:
            return await ctx.reply(
                "No Image was provided, If you want me to make your meme at "
                "least give me something to work with"
            )
        else:
            try:
                cont = msg.content
                member = await BetterMemberConverter().convert(ctx, cont)
                image_url = str(member.avatar.with_static_format("png").with_size(1024))
            except BaseException:
                pass
            if len(msg.attachments) != 0:
                try:
                    image_url = msg.attachments[0].url

                except BaseException:
                    return await msg.reply(
                        "I was unable to use the attachment you provided"
                    )
            elif len(msg.mentions) > 0:
                image_url = str(
                    msg.mentions[0].avatar.with_format("png").with_size(1024))
            else:
                source = msg.content
                val_stat = await UrlValidator().validate(source)
                if val_stat:
                    image_url = str(source)
                else:
                    return await msg.reply('The URL provided was invalid.')
            await msg.reply(
                "Great, now hit me we with the \
        puncline/top text/joke for the "
                "meme. Please note whatever message you send is the content."
            )
            try:
                tm = await self.client.wait_for("message", timeout=60.0,
                                                check=check)
            except asyncio.TimeoutError:
                return await msg.reply(
                    "No top text was provided, If you want me to make your "
                    "meme at least give me something to work with"
                )
            else:
                toptext = tm.content
                img = await self.client.dagpi.image_process(
                    ImageFeatures.modern_meme(), url=image_url, text=toptext)
                await self.img_cog.to_embed(ctx, img, "Meme")
