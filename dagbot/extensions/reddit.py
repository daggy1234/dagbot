import asyncio
from dagbot.utils.context import MyContext
import json
import os
import random
from datetime import datetime
from typing import List, Tuple, TypedDict, Union, Literal

import discord
import humanize
import matplotlib.pyplot as plt
from discord.ext import commands, tasks

class KsoftRedditPayload(TypedDict):
    title: str
    meme: str
    auth: str
    memeurl: str
    ups: str
    auth_url: str


class RedditPayload(TypedDict):
    title: str
    doots: str
    author: str
    post: str
    link: str
    authorurl: str

SUB_ERROR = Tuple[Literal[False], str]
SUB_SUCCESS = Tuple[Literal[True], KsoftRedditPayload]

class reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.memcache.start()

    async def cog_check(self, ctx: MyContext):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                return bool(e["reddit"])

    async def randsub(self, subreddit: str, time="day") -> Union[SUB_ERROR, SUB_SUCCESS]:
        url = f"https://api.ksoft.si/images/rand-reddit/{subreddit}"
        headers = {
            "Authorization": self.client.data['ksofttoken'],
            "remove_nsfw": "true",
        }
        params = {"span": time}
        r = await self.client.session.get(url, params=params, headers=headers)
        file = await r.json()
        try:
            file["error"]
        except BaseException:
            iurl = file["image_url"]
            tit = file["title"]
            u = file["upvotes"]
            auth = file["author"]
            auth = auth.replace("/u", "u")
            authurl = "https://reddit.com/" + auth.replace("/u/", "user/")
            url = file["source"]
            dict_: KsoftRedditPayload = {
                "title": tit,
                "meme": iurl,
                "auth": auth,
                "memeurl": url,
                "ups": u,
                "auth_url": authurl,
            }
            return True, dict_
        else:
            # dict_ = {"success": False, "error": file["message"]}
            return False, file["message"]

    async def sublist(self, sub: str) -> List[RedditPayload]:
        danklist = []
        url = f"https://reddit.com/r/{sub}.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/50.0.2661.102 Safari/537.36"
        }
        y = await self.client.session.get(url, headers=headers)
        r = await y.json()
        memelist = r["data"]["children"]
        for meme in memelist:
            data = meme["data"]
            if data["over_18"] or data['stickied']:
                continue
            auth = "u/" + data["author"]
            auth_url = f"https://reddit.com/user/{data['author']}"
            if data["is_reddit_media_domain"]:
                purl = data["url"]
            elif data["domain"] == "i.imgur.com":
                if data['url'].endswith('.gifv'):
                    purl = data["url"].replace(".gifv", ".gif")
                else:
                    purl = data['url'] + '.gif'
            else:
                purl = data["url"]
            title = data["title"]
            score = data["score"]
            permurl = "https://reddit.com" + data["permalink"]
            memdict: RedditPayload = {
                "author": auth,
                "authorurl": auth_url,
                "post": purl,
                "title": title,
                "doots": score,
                "link": permurl,
            }
            danklist.append(memdict)
        return danklist

    async def memecache(self) -> None:
        try:
            with open("./dagbot/data/memes.json", "r") as file:
                jsdict = json.load(file)
                jsdict["dankmemes"] = list(set(jsdict["dankmemes"] + await self.sublist(
                    "dankmemes")))
                await asyncio.sleep(1)
                jsdict["memes"] = list(set(jsdict["memes"] + await self.sublist("memes")))
                await asyncio.sleep(1)
                jsdict["wholesome"] = list(set(jsdict["wholesome"] + await self.sublist(
                    "wholesomememes"
                )))
        except FileNotFoundError:
            with open("./dagbot/data/memes.json", "x") as file:
                js = json.dumps(
                    {"dankmemes": [], "memes": [], "wholesome": []})
                file.write(js)

            with open("./dagbot/data/memes.json", "r") as file:
                jsdict = json.load(file)
                jsdict["dankmemes"] = jsdict["dankmemes"] + await self.sublist(
                    "dankmemes")
                await asyncio.sleep(1)
                jsdict["memes"] = jsdict["memes"] + await self.sublist("memes")
                await asyncio.sleep(1)
                jsdict["wholesome"] = jsdict["wholesome"] + await self.sublist(
                    "wholesomememes"
                )
        with open("./dagbot/data/memes.json", "w") as file:
            json.dump(jsdict, file)

    @tasks.loop(seconds=7200)
    async def memcache(self):
        try:
            with open("./dagbot/data/memes.json", "r") as file:
                jsdict = json.load(file)
                jsdict["dankmemes"] = jsdict["dankmemes"] + await self.sublist(
                    "dankmemes")
                await asyncio.sleep(1)
                jsdict["memes"] = jsdict["memes"] + await self.sublist("memes")
                await asyncio.sleep(1)
                jsdict["wholesome"] = jsdict["wholesome"] + await self.sublist(
                    "wholesomememes"
                )
            with open("./dagbot/data/memes.json", "w") as file:
                json.dump(jsdict, file)
        except FileNotFoundError:
            with open("./dagbot/data/memes.json", "w") as file:
                jsdict = {"dankmemes": [],"memes": [], "wholesome": []}
                jsdict["dankmemes"] = jsdict["dankmemes"] + await self.sublist(
                    "dankmemes")
                await asyncio.sleep(1)
                jsdict["memes"] = jsdict["memes"] + await self.sublist("memes")
                await asyncio.sleep(1)
                jsdict["wholesome"] = jsdict["wholesome"] + await self.sublist(
                    "wholesomememes"
                )
                json.dump(jsdict, file)
        self.client.logger.debug("MEMES CACHED")

    @memcache.before_loop
    async def before_printer(self):
        self.client.logger.info("WAITING FOR ON READY")
        await self.client.wait_until_ready()

    async def loadmeme(self, sub: str) -> RedditPayload:
        with open("./dagbot/data/memes.json", "r") as file:
            js = json.load(file)
            memelist: List[RedditPayload] = js[sub]
            return random.choice(memelist)

    async def meme_embed(self) -> discord.Embed:
        r = random.randint(0, 2)
        if r == 1:
            sub = "dankmemes"
        elif r == 2:
            sub = "memes"
        else:
            sub = "wholesome"
        meme = await self.loadmeme(sub)
        embed = discord.Embed(
            title=meme["title"], url=meme["link"]
        )
        embed.set_author(name=meme["author"], url=meme["authorurl"])
        embed.add_field(name="Upvotes", value=meme["doots"], inline=True)
        url = str(meme["post"])
        embed.set_image(url=url)
        return embed

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def meme(self, ctx: MyContext):
        embed = await self.meme_embed()
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def comic(self, ctx: MyContext):
        await ctx.typing()
        channel = ctx.channel
        guild = ctx.guild
        suc, meme = await self.randsub("comics")
        if isinstance(meme, str):
            return await ctx.send(meme)

        embed = discord.Embed(
            title=meme["title"], color=guild.me.color, url=meme["memeurl"]
        )
        embed.set_author(name=meme["auth"], url=meme["auth_url"])
        embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
        url = str(meme["meme"])
        embed.set_image(url=url)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True,
                      aliases=["pqmeme", "PrequelMemes"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def starwarsmeme(self, ctx: MyContext):
        await ctx.typing()
        channel = ctx.channel
        guild = ctx.guild
        suc, meme = await self.randsub("PrequelMemes")
        if isinstance(meme, str):
            return await ctx.send(meme)

        embed = discord.Embed(
            title=meme["title"], color=guild.me.color, url=meme["memeurl"]
        )
        embed.set_author(name=meme["auth"], url=meme["auth_url"])
        embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
        url = str(meme["meme"])
        embed.set_image(url=url)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def aww(self, ctx: MyContext):
        await ctx.typing()
        return await ctx.send(
            "Please use the animals instead. r/aww is pretty meh")

    @commands.command(cooldown_after_parsing=True,
                      aliases=["dankex", "exchange"], hidden=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dex(self, ctx: MyContext):
        await ctx.typing()
        channel = ctx.channel
        guild = ctx.guild
        suc, meme = await self.randsub("DankExchange")
        if isinstance(meme, str):
            return await ctx.send(meme)

        embed = discord.Embed(
            title=meme["title"], color=guild.me.color, url=meme["memeurl"]
        )
        embed.set_author(name=meme["auth"], url=meme["auth_url"])
        embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
        url = str(meme["meme"])
        embed.set_image(url=url)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=["ii"], hidden=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def investorinfo(self, ctx: MyContext, *, ruser: str = None):
        if not ruser:
            return await ctx.send("Hey please specify a reddit user")
        r = await self.client.session.get(
            f"https://dankexchange.io/api/investors/{ruser}")
        if r.status == 404:
            return await ctx.send(
                f"`{ruser}` does not exist on r/DankExchange. Ask them to create a profile.")
        elif r.status == 200:
            js = await r.json()
            embed = discord.Embed(title=f"Investor: u/{js['username']}")
            embed.description = f"[Reddit](https://reddit.com/u/{ruser}) | [Dankexchange.io](https://dankexchange.io/investor/{ruser}) "
            embed.add_field(name="Balance", value=js["balance"])
            embed.add_field(name="Net Worth", value=js["net_worth"])
            embed.add_field(name="Rank (NW)", value=js["net_worth_rank"])
            embed.add_field(
                name="RP",
                value=f"Ranked `{js['ranked_points']}` with tier `{js['ranked_tier']}`")
            embed.add_field(
                name="Firm",
                value=f"In firm id:`{js['firm_id']}` with position `{js['firm_role']}`")
            rs_info = await self.client.session.get(
                f"https://www.reddit.com/user/{ruser}/about.json")
            jso = await rs_info.json()
            im = jso["data"]["icon_img"].split("?")[0]
            embed.set_thumbnail(url=im)
            embed.set_footer(
                text=f"Reddit Account created: {humanize.naturaltime(datetime.utcnow() - datetime.fromtimestamp(jso['data']['created_utc']))}")
            return await ctx.send(embed=embed)
        else:
            return await ctx.send("Error Occured. Status code {r.status}")

    @commands.command(cooldown_after_parsing=True, aliases=["fi", "firm"],
                      hidden=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def firminfo(self, ctx, *, firm_str: str = None):
        if not firm_str:
            return await ctx.send("Please specify a valid firm id")
        try:
            firm = int(firm_str)
        except ValueError:
            return await ctx.send(
                "Please specify a valid firm id. Not the name of the firm")
        r = await self.client.session.get(
            f"https://dankexchange.io/api/firms/{firm}")
        if r.status == 404:
            return await ctx.send(f"Firm of id `{firm}` does not exist.")
        elif r.status == 200:
            js = await r.json()
            embed = discord.Embed(title=f"Firm Info: {js['name']}")
            embed.add_field(name="Id", value=firm)
            embed.add_field(
                name="Ceo",
                value=f"[{js['ceo']}](https://dankexchange.io/investor/{js['ceo']})")
            embed.add_field(name="Member Count",
                            value=f"{js['member_count']}/{js['member_limit']}")
            embed.add_field(name="Status", value=f"Firm is {js['status']}")
            embed.add_field(
                name="location",
                value=f"Moved to {js['location_name']} {humanize.naturaltime(datetime.utcnow() - datetime.fromtimestamp(js['last_move_time']))}")
            embed.add_field(
                name="Stats",
                value=f"Tax Rate: {js['location_tax_rate']}\nBenifit: {js['location_bonus']}")
            members = js['members']
            members.remove(js['ceo'])
            embed.description = "**Members**\n" + ",".join(
                f"[{mem}](https://dankexchange.io/investor/{mem})"
                for mem in members
            )

            return await ctx.send(embed=embed)
        else:
            return await ctx.send("Error Occured. Status code {r.status}")

    @commands.command(cooldown_after_parsing=True, aliases=["dm"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def discord(self, ctx: MyContext):
        await ctx.typing()
        channel = ctx.channel
        guild = ctx.guild
        suc, meme = await self.randsub("discord")
        if isinstance(meme, str):
            return await ctx.send(meme)

        embed = discord.Embed(
            title=meme["title"], color=guild.me.color, url=meme["memeurl"]
        )
        embed.set_author(name=meme["auth"], url=meme["auth_url"])
        embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
        url = str(meme["meme"])
        embed.set_image(url=url)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def facepalm(self, ctx: MyContext):
        await ctx.typing()
        channel = ctx.channel
        guild = ctx.guild
        suc, meme = await self.randsub("facepalm")
        if isinstance(meme, str):
            return await ctx.send(meme)

        embed = discord.Embed(
            title=meme["title"], color=guild.me.color, url=meme["memeurl"]
        )
        embed.set_author(name=meme["auth"], url=meme["auth_url"])
        embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
        url = str(meme["meme"])
        embed.set_image(url=url)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def meirl(self, ctx: MyContext):
        await ctx.typing()
        channel = ctx.channel
        guild = ctx.guild
        suc, meme = await self.randsub("me_irl")
        if isinstance(meme, str):
            return await ctx.send(meme)

        embed = discord.Embed(
            title=meme["title"], color=guild.me.color, url=meme["memeurl"]
        )
        embed.set_author(name=meme["auth"], url=meme["auth_url"])
        embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
        url = str(meme["meme"])
        embed.set_image(url=url)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True,
                      aliases=["4chan", "fourchan"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def greentext(self, ctx: MyContext):
        await ctx.typing()
        channel = ctx.channel
        guild = ctx.guild
        suc, meme = await self.randsub("greentext")
        if isinstance(meme, str):
            return await ctx.send(meme)

        embed = discord.Embed(
            title=meme["title"], color=guild.me.color, url=meme["memeurl"]
        )
        embed.set_author(name=meme["auth"], url=meme["auth_url"])
        embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
        url = str(meme["meme"])
        embed.set_image(url=url)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sub(self, ctx, subreddit: str, time: str = "day"):
        time = time.lower()
        guild = ctx.guild
        suc, meme = await self.randsub(subreddit, time)
        if isinstance(meme, str):
            return await ctx.send(meme)
        embed = discord.Embed(
            title=meme["title"], color=guild.me.color, url=meme["memeurl"]
        )
        embed.add_field(name="User", value=meme["auth"], inline=True)
        embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
        url = str(meme["memeurl"])
        embed.set_image(url=url)
        embed.set_footer(text=subreddit)
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dexuv(self, ctx, *, pid: str):
        burl = self.client.data["dankapi"]
        url = burl + pid
        r = await self.client.session.get(url)
        js = await r.json()

        try:
            len(js["x"]) - 1
        except BaseException:
            await ctx.send(
                "No data, please enter a valid post id from r/DankExchange"
            )
        else:
            def makegraph():
                plt.xlabel("Time in Minutes")
                plt.ylabel("Upvotes")
                y = js["y"]
                plt.plot(
                    y,
                    color="black",
                    marker="o",
                    linestyle="dashed",
                    linewidth=1,
                    markersize=6,
                )
                plt.savefig(f"{pid}graph.png")
                plt.close()

            await self.client.loop.run_in_executor(None, makegraph)
            file = discord.File(f"{pid}graph.png", filename="graph.png")
            embed = discord.Embed(
                title=f"Upvote Graph for {pid}",
                color=ctx.guild.me.color)
            embed.set_image(url="attachment://graph.png")
            embed.set_footer(
                text="Powered by C🅰ri🅱🅾s🅰urus#0834 Dank Exchange API")
            await ctx.send(file=file, embed=embed)
            os.remove(f"{pid}graph.png")


async def setup(client):
    await client.add_cog(reddit(client))
