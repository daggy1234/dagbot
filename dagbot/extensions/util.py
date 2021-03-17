import random

import async_cse
import discord
from jishaku import codeblocks
from bs4 import BeautifulSoup
from discord.ext import commands, menus
from discord.ext.commands import BucketType


def setup(client):
    client.add_cog(util(client))


class MyMenuyt(menus.Menu):
    def __init__(self, y):
        super().__init__()
        self.y = y

    async def send_initial_message(self, ctx, channel):
        embed = discord.Embed(
            title=self.y["title"][0],
            url=self.y["urls"][0],
            description=f"""
    {self.y['channel'][0]} on {self.y['time'][0]}""",
            color=self.ctx.guild.me.color,
        )
        embed.add_field(
            name="------------------------",
            value=self.y["description"][0],
            inline=False,
        )
        embed.set_thumbnail(url=self.y["thumbnails"][0])
        return await channel.send(embed=embed)

    @menus.button("1\N{combining enclosing keycap}")
    async def result_1(self, payload):
        embed = discord.Embed(
            title=self.y["title"][0],
            url=self.y["urls"][0],
            description=f"""
    {self.y['channel'][0]} on {self.y['time'][0]}""",
            color=self.ctx.guild.me.color,
        )
        embed.add_field(
            name="------------------------",
            value=self.y["description"][0],
            inline=False,
        )
        embed.set_thumbnail(url=self.y["thumbnails"][0])
        await self.message.edit(embed=embed)

    @menus.button("2\N{combining enclosing keycap}")
    async def result_2(self, payload):
        embed = discord.Embed(
            title=self.y["title"][1],
            url=self.y["urls"][1],
            description=f"""
    {self.y['channel'][1]} on {self.y['time'][1]}""",
            color=self.ctx.guild.me.color,
        )
        embed.add_field(
            name="------------------------",
            value=self.y["description"][1],
            inline=False,
        )
        embed.set_thumbnail(url=self.y["thumbnails"][1])
        await self.message.edit(embed=embed)

    @menus.button("3\N{combining enclosing keycap}")
    async def result_3(self, payload):
        embed = discord.Embed(
            title=self.y["title"][2],
            url=self.y["urls"][2],
            description=f"""
    {self.y['channel'][2]} on {self.y['time'][2]}""",
            color=self.ctx.guild.me.color,
        )
        embed.add_field(
            name="------------------------",
            value=self.y["description"][2],
            inline=False,
        )
        embed.set_thumbnail(url=self.y["thumbnails"][2])
        await self.message.edit(embed=embed)

    @menus.button("4\N{combining enclosing keycap}")
    async def result_4(self, payload):
        embed = discord.Embed(
            title=self.y["title"][3],
            url=self.y["urls"][3],
            description=f"""
    {self.y['channel'][3]} on {self.y['time'][3]}""",
            color=self.ctx.guild.me.color,
        )
        embed.add_field(
            name="------------------------",
            value=self.y["description"][3],
            inline=False,
        )
        embed.set_thumbnail(url=self.y["thumbnails"][3])
        await self.message.edit(embed=embed)

    @menus.button("5\N{combining enclosing keycap}")
    async def result_5(self, payload):
        embed = discord.Embed(
            title=self.y["title"][4],
            url=self.y["urls"][4],
            description=f"""
    {self.y['channel'][4]} on {self.y['time'][4]}""",
            color=self.ctx.guild.me.color,
        )
        embed.add_field(
            name="------------------------",
            value=self.y["description"][4],
            inline=False,
        )
        embed.set_thumbnail(url=self.y["thumbnails"][4])
        await self.message.edit(embed=embed)

    @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def on_stop(self, payload):
        self.stop()


class MyMenugoogle(menus.Menu):
    def __init__(self, reslist):
        super().__init__()
        self.reslist = reslist

    async def send_initial_message(self, ctx, channel):
        return await channel.send(self.reslist[0].url)

    @menus.button("1\N{combining enclosing keycap}")
    async def result_one(self, payload):
        await self.message.edit(content=self.reslist[0].url)

    @menus.button("2\N{combining enclosing keycap}")
    async def result_2(self, payload):
        await self.message.edit(content=self.reslist[1].url)

    @menus.button("3\N{combining enclosing keycap}")
    async def result_3(self, payload):
        await self.message.edit(content=self.reslist[2].url)

    @menus.button("4\N{combining enclosing keycap}")
    async def result_4(self, payload):
        await self.message.edit(content=self.reslist[3].url)

    @menus.button("5\N{combining enclosing keycap}")
    async def result_5(self, payload):
        await self.message.edit(content=self.reslist[4].url)

    @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def on_stop(self, payload):
        self.stop()


class util(commands.Cog):
    """useful features (might actually help)"""

    def __init__(self, client):
        self.client = client
        self.googlethingy = async_cse.Search(self.client.data["gapikey"])

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                return bool(e["util"])

    async def get_wiki(self, query):
        url = "https://en.wikipedia.org/w/api.php?action=query&prop=" \
              "extracts&exsentences=4&exlimit=1&titles={}&explaintext=1&" \
              "formatversion=2&format=json".format(query)
        response = await self.client.session.get(url)
        file = await (response.json())
        tit = file["query"]["pages"][0]["title"]
        conten = file["query"]["pages"][0]["extract"]
        furl = "https://en.wikipedia.org/wiki/" + tit
        return {"title": tit, "content": conten, "url": furl}

    async def gettaco(self):
        response = await self.client.session.get(
            "http://taco-randomizer.herokuapp.com")
        file = await response.read()
        soup = BeautifulSoup(file, "html.parser")
        head = str(soup.body.find("h1", attrs={"class": "light"}).Text)
        ll = [link.get("href") for link in soup.find_all("a")]
        perma = f"http://taco-randomizer.herokuapp.com{str(ll[1])}"
        return {"text": head, "link": perma}

    async def ytget(self, query):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=" \
              f"{query}&key={self.client.data['gapikey']}"
        response = await self.client.session.get(url)
        resp = await response.json()
        titlist = []
        desclist = []
        thumblist = []
        urlist = []
        chanlist = []
        timlist = []
        kindlist = []
        if len(resp["items"]) == 0:
            return {"title": False}
        for r in resp["items"]:
            kind = r["id"]["kind"]
            if kind == "youtube#channel":
                id = r["id"]["channelId"]
                urlist.append(f"https://www.youtube.com/channel/{id}")
            elif kind == "youtube#video":
                id = r["id"]["videoId"]
                urlist.append(f"https://www.youtube.com/watch?v={id}")
            else:
                urlist.append(
                    "https://i1.wp.com/www.rattleandmum.co.za/wp-content/"
                    "uploads/2015/02/IMG_0102.png"
                )
            titlist.append(r["snippet"]["title"])
            desclist.append(r["snippet"]["description"])
            thumblist.append(r["snippet"]["thumbnails"]["default"]["url"])
            timlist.append(r["snippet"]["publishedAt"])
            chanlist.append(r["snippet"]["channelTitle"])
        return {
            "title": titlist,
            "description": desclist,
            "thumbnails": thumblist,
            "urls": urlist,
            "channel": chanlist,
            "time": timlist,
            "kind": kindlist,
        }

    async def get_weather(self, y):
        response = await self.client.session.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={y}&"
            f"appid={self.client.data['weatherapi']}"
        )
        file = await response.json()
        try:
            temp = file["main"]["temp"]
        except BaseException:
            return file["message"]
        else:
            realfeel = file["main"]["feels_like"]
            temp = file["main"]["temp"]
            realfeel = file["main"]["feels_like"]
            tempmin = file["main"]["temp_min"]
            tempmax = file["main"]["temp_max"]
            pressure = file["main"]["pressure"]
            humdidity = file["main"]["humidity"]
            tempc = round(temp - 273, 2)
            realfeelc = round(realfeel - 273, 2)
            tempmaxc = round(tempmax - 273, 2)
            tempminc = round(tempmin - 273, 2)
            tempf = round((temp * 1.8) - 460, 2)
            realfeelf = round((realfeel * 1.8) - 460, 2)
            tempmaxf = round((tempmax * 1.8) - 460, 2)
            tempminf = round((tempmin * 1.8) - 460, 2)
            return """```
{},{}
{}
{}
Temperature:           {}C/{}F
TEMPERATURE REAL FEEL: {}C/{}F
TEMPERATURE MAXIMUM:   {}C/{}F
TEMPERATURE MINIMUM:   {}C/{}F
HUMIDITY:              {}%
pressure:              {}hPa```""".format(
                file["name"],
                file["sys"]["country"],
                file["weather"][0]["main"],
                file["weather"][0]["description"],
                tempc,
                tempf,
                realfeelc,
                realfeelf,
                tempmaxc,
                tempmaxf,
                tempminc,
                tempminf,
                humdidity,
                pressure,
            )

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 20, type=commands.BucketType.user)
    async def google(self, ctx, *, query: str):
        channel = ctx.channel
        qu, st = await self.client.bwordchecker.bwordcheck(query)
        if qu:
            if not channel.is_nsfw():
                return await ctx.send(
                    f"You have used an NSFW command search query in a "
                    f"Safe for Work channel\n{st}"
                )

            reslist = await self.googlethingy.search(query)
        else:
            reslist = await self.googlethingy.search(query, safesearch=True)
        if len(reslist) == 0:
            return await ctx.send("NO RESULTS")
        m = MyMenugoogle(reslist)
        await m.start(ctx)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 120, type=commands.BucketType.user)
    async def weather(self, message, *, city: str):
        channel = message.channel
        y = str(city)
        result = await self.get_weather(y)
        await channel.send(result)

    @commands.command(cooldown_after_parsing=True, aliases=["random"])
    async def randomint(self, message, start: int, end: int):
        channel = message.channel
        guild = message.guild
        embed = discord.Embed(
            title="DAGBOT - RANDOM INTEGER",
            color=guild.me.color)
        y = int(start)
        z = int(end)
        if z >= y:
            x = random.randint(y, z)
            embed.add_field(name="RANDOM INTEGER", value=x, inline=False)
        else:
            embed.add_field(
                name="RANDOM INTEGER EROOR",
                value="Start range number is greater than end",
                inline=False,
            )

        await channel.send(embed=embed)

    @commands.command(
        cooldown_after_parsing=True, aliases=["random taco", "rtaco", "rt"]
    )
    async def taco(self, ctx):
        guild = ctx.guild
        await ctx.trigger_typing()
        tcor = await self.gettaco()
        embed = discord.Embed(
            title="DAGBOT - RANDOM TACO",
            color=guild.me.color)
        embed.add_field(name="TACO", value=tcor["text"], inline=False)
        embed.add_field(name="LINK (recipe)", value=tcor["link"], inline=False)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=["wiki", "pedia"])
    async def wikipedia(self, ctx, *, query):
        channel = ctx.channel
        qu, st = await self.client.bwordchecker.bwordcheck(query)
        if (not qu or not channel.is_nsfw()) and qu:
            return await ctx.send(
                f"You have used an NSFW command search query in a "
                f"Safe for Work channel\n{st}"
            )

        await ctx.trigger_typing()
        resp = await self.get_wiki(query)
        color = ctx.guild.me.color
        title = resp["title"]
        url = resp["url"]
        con = resp["content"]
        embed = discord.Embed(
            title=title, url=url, description=con, color=color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=["yt"])
    async def youtube(self, ctx, *, query):
        channel = ctx.channel
        qu, st = await self.client.bwordchecker.bwordcheck(query)
        if (not qu or not channel.is_nsfw()) and qu:
            return await ctx.send(
                f"You have used an NSFW command search query in a "
                f"Safe for Work channel\n{st}"
            )

        await ctx.trigger_typing()
        y = await self.ytget(query)
        if not y["title"]:
            return await ctx.send("No results")
        m = MyMenuyt(y)
        await m.start(ctx)

    @commands.command(aliases=["dagpaste"])
    @commands.cooldown(1, 30, BucketType.user)
    async def paste(self, ctx, *, paste: str = None):
        if not paste and not ctx.message.attachments:
            return await ctx.send("No Paste Data")
        elif not paste:
            attachments = ctx.message.attachments
            if attachments[0].height:
                return await ctx.send(
                    "That file has a height, meaning it's probably an image. I can't paste those!")
            if attachments[0].size // 1000000 > 8:
                return await ctx.send("That's too large of a file!")
            split_attachment = attachments[0].filename.split(".")
            if split_attachment[1] in ["zip", "exe", "nbt"]:
                return await ctx.send(
                    f"Invalid file type: `{split_attachment[1]}` is invalid.")
            file = await attachments[0].read()
            text = file.decode('UTF-8')
            url = await self.client.session.post("https://paste.daggy.tech/upload", data=text)
            js = await url.json()
            return await ctx.send(js["file"])
        elif not ctx.message.attachments:
            paste = codeblocks.codeblock_converter(paste)
            lang = paste[0] or ""
            url = await self.client.session.post("https://paste.daggy.tech/upload", data=paste[1])
            js = await url.json()
            return await ctx.send(f'{js["file"]}.{lang}')
