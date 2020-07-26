import asyncio
import json
import os
import random

import aiohttp
import discord
import humanize
import matplotlib.pyplot as plt
from discord.ext import commands, tasks


class reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.memcache.start()

    async def cog_check(self, ctx):
        id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(id):
                if e["reddit"]:
                    return True
                else:
                    return False

    async def randsub(self, subreddit, time="day"):
        url = f"https://api.ksoft.si/images/rand-reddit/{subreddit}"
        headers = {
            "Authorization": self.client.data['ksofttoken'],
            "remove_nsfw": "true",
        }
        params = {"span": time}
        r = await self.client.session.get(url, params=params, headers=headers)
        file = await r.json()
        try:
            y = file["error"]
        except BaseException:
            iurl = file["image_url"]
            tit = file["title"]
            sub = file["subreddit"]
            u = file["upvotes"]
            auth = file["author"]
            auth = auth.replace("/u", "u")
            authurl = "https://reddit.com/" + auth.replace("/u/", "user/")
            url = file["source"]
            dict = {
                "success": True,
                "title": tit,
                "meme": iurl,
                "auth": auth,
                "memeurl": url,
                "ups": u,
                "auth_url": authurl,
            }
            return dict
        else:
            dict = {"success": False, "error": file["message"]}
            return dict

    async def sublist(self, sub):
        danklist = []
        url = f"https://reddit.com/r/{sub}.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        y = await self.client.session.get(url, headers=headers)
        r = await y.json()
        memelist = r["data"]["children"]
        for meme in memelist:
            data = meme["data"]
            if data["over_18"] == True:
                continue
            else:
                auth = "u/" + data["author"]
                auth_url = f"https://reddit.com/user/{data['author']}"
                if data["is_reddit_media_domain"] == True:
                    purl = data["url"]
                elif data["domain"] == "i.imgur.com":
                    purl = data["url"].replace(".gifv", ".gif")
                else:
                    purl = data["url"]
                title = data["title"]
                score = data["score"]
                permurl = "https://reddit.com" + data["permalink"]
            memdict = {
                "author": auth,
                "authorurl": auth_url,
                "post": purl,
                "title": title,
                "doots": score,
                "link": permurl,
            }
            danklist.append(memdict)
        return danklist

    async def memecache(self):
        with open("./dagbot/data/memes.json", "r") as file:
            jsdict = json.load(file)
            jsdict["dankmemes"] = jsdict["dankmemes"] + await self.sublist("dankmemes")
            await asyncio.sleep(1)
            jsdict["memes"] = jsdict["memes"] + await self.sublist("memes")
            await asyncio.sleep(1)
            jsdict["wholesome"] = jsdict["wholesome"] + await self.sublist(
                "wholesomememes"
            )
        with open("./dagbot/data/memes.json", "w") as file:
            json.dump(jsdict, file)
        print("Memes Cached")

    @tasks.loop(seconds=7200)
    async def memcache(self):
        with open("./dagbot/data/memes.json", "r") as file:
            jsdict = json.load(file)
            jsdict["dankmemes"] = jsdict["dankmemes"] + await self.sublist("dankmemes")
            await asyncio.sleep(1)
            jsdict["memes"] = jsdict["memes"] + await self.sublist("memes")
            await asyncio.sleep(1)
            jsdict["wholesome"] = jsdict["wholesome"] + await self.sublist(
                "wholesomememes"
            )
        with open("./dagbot/data/memes.json", "w") as file:
            json.dump(jsdict, file)
        print("Memes Cached")

    @memcache.before_loop
    async def before_printer(self):
        print("waiting...")
        await self.client.wait_until_ready()

    async def loadmeme(self, sub):
        with open("./dagbot/data/memes.json", "r") as file:
            js = json.load(file)
            memelist = js[sub]
            memdict = random.choice(memelist)
            return memdict
            file.close()

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def meme(self, ctx):
        r = random.randint(0, 2)
        if r == 1:
            sub = "dankmemes"
        elif r == 2:
            sub = "memes"
        else:
            sub = "wholesome"
        await ctx.trigger_typing()
        meme = await self.loadmeme(sub)
        embed = discord.Embed(
            title=meme["title"], color=ctx.guild.me.color, url=meme["link"]
        )
        embed.set_author(name=meme["author"], url=meme["authorurl"])
        embed.add_field(name="Upvotes", value=meme["doots"], inline=True)
        url = str(meme["post"])
        embed.set_image(url=url)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def comic(self, ctx):
        await ctx.trigger_typing()
        await ctx.trigger_typing()
        channel = ctx.channel
        guild = ctx.guild
        meme = await self.randsub("comics")
        if meme["success"]:
            embed = discord.Embed(
                title=meme["title"], color=guild.me.color, url=meme["memeurl"]
            )
            embed.set_author(name=meme["auth"], url=meme["auth_url"])
            embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
            url = str(meme["meme"])
            embed.set_image(url=url)
            await channel.send(embed=embed)
        else:
            return await ctx.send(meme["error"])

    @commands.command(cooldown_after_parsing=True,
                      aliases=["pqmeme", "PrequelMemes"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def starwarsmeme(self, ctx):
        await ctx.trigger_typing()
        channel = ctx.channel
        guild = ctx.guild
        meme = await self.randsub("PrequelMemes")
        if meme["success"]:
            embed = discord.Embed(
                title=meme["title"], color=guild.me.color, url=meme["memeurl"]
            )
            embed.set_author(name=meme["auth"], url=meme["auth_url"])
            embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
            url = str(meme["meme"])
            embed.set_image(url=url)
            await channel.send(embed=embed)
        else:
            return await ctx.send(meme["error"])

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def aww(self, ctx):
        await ctx.trigger_typing()
        channel = ctx.channel
        guild = ctx.guild
        return await ctx.send("Please use the animals instead. r/aww is pretty meh")

    @commands.command(cooldown_after_parsing=True,
                      aliases=["dankex", "exchange"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dex(self, ctx):
        await ctx.trigger_typing()
        channel = ctx.channel
        guild = ctx.guild
        meme = await self.randsub("DankExchange")
        if meme["success"]:
            embed = discord.Embed(
                title=meme["title"], color=guild.me.color, url=meme["memeurl"]
            )
            embed.set_author(name=meme["auth"], url=meme["auth_url"])
            embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
            url = str(meme["meme"])
            embed.set_image(url=url)
            await channel.send(embed=embed)
        else:
            return await ctx.send(meme["error"])

    @commands.command(cooldown_after_parsing=True, aliases=["dm"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def discord(self, ctx):
        await ctx.trigger_typing()
        channel = ctx.channel
        guild = ctx.guild
        meme = await self.randsub("discord")
        if meme["success"]:
            embed = discord.Embed(
                title=meme["title"], color=guild.me.color, url=meme["memeurl"]
            )
            embed.set_author(name=meme["auth"], url=meme["auth_url"])
            embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
            url = str(meme["meme"])
            embed.set_image(url=url)
            await channel.send(embed=embed)
        else:
            return await ctx.send(meme["error"])

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def facepalm(self, ctx):
        await ctx.trigger_typing()
        channel = ctx.channel
        guild = ctx.guild
        meme = await self.randsub("facepalm")
        if meme["success"]:
            embed = discord.Embed(
                title=meme["title"], color=guild.me.color, url=meme["memeurl"]
            )
            embed.set_author(name=meme["auth"], url=meme["auth_url"])
            embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
            url = str(meme["meme"])
            embed.set_image(url=url)
            await channel.send(embed=embed)
        else:
            return await ctx.send(meme["error"])

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def meirl(self, ctx):
        await ctx.trigger_typing()
        channel = ctx.channel
        guild = ctx.guild
        meme = await self.randsub("me_irl")
        if meme["success"]:
            embed = discord.Embed(
                title=meme["title"], color=guild.me.color, url=meme["memeurl"]
            )
            embed.set_author(name=meme["auth"], url=meme["auth_url"])
            embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
            url = str(meme["meme"])
            embed.set_image(url=url)
            await channel.send(embed=embed)
        else:
            return await ctx.send(meme["error"])

    @commands.command(cooldown_after_parsing=True,
                      aliases=["4chan", "fourchan"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def greentext(self, ctx):
        await ctx.trigger_typing()
        channel = ctx.channel
        guild = ctx.guild
        meme = await self.randsub("greentext")
        if meme["success"]:
            embed = discord.Embed(
                title=meme["title"], color=guild.me.color, url=meme["memeurl"]
            )
            embed.set_author(name=meme["auth"], url=meme["auth_url"])
            embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
            url = str(meme["meme"])
            embed.set_image(url=url)
            await channel.send(embed=embed)
        else:
            return await ctx.send(meme["error"])

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sub(self, ctx, subreddit: str, time: str = "day"):
        time = time.lower()
        guild = ctx.guild
        meme = await self.randsub(subreddit, time)
        if meme["success"]:
            embed = discord.Embed(
                title=meme["title"], color=guild.me.color, url=meme["memeurl"]
            )
            embed.add_field(name="User", value=meme["maker"], inline=True)
            embed.add_field(name="Upvotes", value=meme["ups"], inline=True)
            url = str(meme["memeimage"])
            embed.set_image(url=url)
            embed.set_footer(text=meme["sub"])
            return await ctx.send(embed=embed)
        else:
            return await ctx.send(meme["error"])

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dexuv(self, ctx, *, pid: str):
        burl = self.client.data["dankapi"]
        url = burl + pid
        r = await self.client.session.get(url)
        js = await r.json()

        try:
            it = len(js["x"]) - 1
        except BaseException:
            await ctx.send(
                "No data, please enter a valid post id from r/DankExchange"
            )
        else:
            def makegraph():
                plt.xlabel("Time in Minutes")
                plt.ylabel("Upvotes")
                x = js["x"]
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
            res = await self.client.loop.run_in_executor(None, makegraph)
            file = discord.File(f"{pid}graph.png", filename="graph.png")
            embed = discord.Embed(
                title=f"Upvote Graph for {pid}",
                color=ctx.guild.me.color)
            embed.set_image(url="attachment://graph.png")
            embed.set_footer(
                text="Powered by C🅰ri🅱🅾s🅰urus#0834 Dank Exchange API")
            await ctx.send(file=file, embed=embed)
            os.remove(f"{pid}graph.png")


def setup(client):
    client.add_cog(reddit(client))
