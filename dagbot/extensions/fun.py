import asyncio
from operator import add
from dagbot.bot import Dagbot
import json
import random
import time
from ipaddress import IPv4Address, IPv6Address
from random import getrandbits
from typing import List, Tuple, Union
from dagbot.utils.daggypag import DaggyPaginator
from dagbot.utils.context import MyContext
import discord
from bs4 import BeautifulSoup
from discord.ext import commands



class fun(commands.Cog):
    """funniest stuff you will ever see"""

    def __init__(self, client: Dagbot):
        self.client = client

    async def cog_check(self, ctx: MyContext):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                return bool(e["fun"])

    async def get_joke(self) -> str:
        header = {"Accept": "application/json"}
        url = "https://icanhazdadjoke.com/"
        r = await self.client.session.get(url, headers=header)
        html = await r.json()
        return html["joke"]

    async def getinpir(self) -> str:
        r = await self.client.session.get(
            'https://inspirobot.me/api?generate=true')
        text = await r.text()
        return text

    async def get_giffy(self, query) -> List[str]:
        url = "https://api.giphy.com/v1/gifs/search"
        querystring = {
            "q": "{}".format(query),
            "api_key": self.client.data['giphykey'],
            "rating": "g"
        }
        response = await self.client.session.get(url, params=querystring)
        cul = await (response.json())
        urllist = []
        if cul["pagination"]["total_count"] == 0:
            urllist[0] = 0
        else:
            for i in range(4):
                urllist.append(cul["data"][i]["images"]["original"]["url"])
            return urllist
        urllist[0] = 0
        return urllist

    async def corp(self) -> str:
        response = await self.client.session.get(
            "https://corporatebs-generator.sameerkumar.website")
        file = await response.json()
        return file["phrase"]

    async def get_advice(self) -> str:
        url = "https://api.adviceslip.com/advice"
        response = await self.client.session.get(url)
        file = await json.loads(await response.text())
        return file["slip"]["advice"]

    async def chuck_norris(self) -> str:
        response = await self.client.session.get(
            "https://api.chucknorris.io/jokes/random")
        file = await response.json()
        return file["value"]

    async def getcomi(self) -> Union[bool, Tuple[str, str, int]]:
        y = random.randint(1, 2485)
        url = f"https://xkcd.com/{y}/"
        r = await self.client.session.get(url)
        html = await r.text()
        soup = BeautifulSoup(html, "html.parser")
        res = soup.find("div", id="comic")
        if res:
            title = str(res.img["title"])
            url = f"https:{res.img['src']}"
            return title, url, y
        return False

    @commands.command(cooldown_after_parsing=True)
    async def ping(self, ctx: MyContext):
        start = time.perf_counter()
        message = await ctx.send("Nope Not gonna do that")
        end = time.perf_counter()
        duration = (end - start) * 1000
        client_lat = round((self.client.latency * 1000), 2)
        await asyncio.sleep(2)
        dp = round(await self.client.dagpi.data_ping(), 2)
        await message.edit(
            content="I'm Weak\ndiff\nPONG!\n- Websocket Latency:"
                    "{} ms\n+ Message {:.2f}\nDagpi: {}".format(client_lat,
                                                                   duration,
                                                                   dp))

    @commands.command(cooldown_after_parsing=True)
    async def dadjoke(self, ctx: MyContext):
        await ctx.trigger_typing()
        guild = ctx.guild
        y = await self.get_joke()
        embed = discord.Embed(
            title="DAGBOT - JOKE", description=y, color=guild.me.color
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, hidden=True)
    async def peace(self, ctx: MyContext):
        guild = ctx.guild
        embed = discord.Embed(title="DAGBOT - PEACE", color=guild.me.color)
        embed.add_field(
            name="PEACE",
            value="AMEN! PEACE IN OUR TIME {}".format(ctx.author),
            inline=True,
        )
        return await ctx.send(embed=embed)

    @commands.command(
        cooldown_after_parsing=True, aliases=["corp", "acorporate", "askcorp"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def askcorporate(self, ctx, *, query):
        await ctx.trigger_typing()
        y = await self.corp()
        guild = ctx.guild
        embed = discord.Embed(
            title="DAGBOT - Ask Corporate",
            description="Question:   {}\nCorporate: {} ".format(query, y),
            color=guild.me.color,
        )
        embed.set_thumbnail(
            url="https://files.taxfoundation.org/20170111174030/corporate.jpg"
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, aliases=["coin", "flip"])
    async def coinflip(self, ctx: MyContext):
        res = random.randint(1, 2)
        guild = ctx.guild
        # heads = 'http://www.virtualcointoss.com/img/quarter_front.png'55
        # tails = 'http://www.virtualcointoss.com/img/quarter_back.png'
        embed = discord.Embed(
            title="Dagbot Coin Flip: Heads",
            color=guild.me.color)
        embed.set_image(
            url= "http://www.virtualcointoss.com/img/quarter_front.png" if res == 1 else "http://www.virtualcointoss.com/img/quarter_back.png")
        return await ctx.send(embed=embed)

    # @commands.command(cooldown_after_parsing=True)
    # @commands.cooldown(1, 3, commands.BucketType.user)
    # async def yomama(self, message):
    #     channel = message.channel
    #     guild = message.guild
    #     response = await self.client.session.get("https://api.yomomma.info/")
    #     yomama = await response.json(content_type=None)
    #     embed = discord.Embed(title="DAGBOT - YOMAMA", color=guild.me.color)
    #     embed.add_field(
    #         name="yomama",
    #         value=(
    #             "{}".format(
    #                 yomama["joke"])),
    #         inline=True)
    #     await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def randam(self, ctx: MyContext):
        embed = discord.Embed(title="Number: 4", color=ctx.guild.me.color)
        embed.set_image(url="https://imgs.xkcd.com/comics/random_number.png")
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def slap(self, message, user: discord.Member):
        channel = message.channel
        guy = str(user.display_name)
        send = str(message.author.display_name)
        if (guy) == str(send):
            await channel.send(
                "**DAGBOT DOES NOTHING {}**\n You cannot slap yourself".format(
                    send)
            )
        elif str(guy) in ["DAGBOT", "dagbot", "Dagbot"]:
            await channel.send(
                "WELL **DAGBOT SENDS A SLAP TO {}**".format(send))
        else:
            await channel.send("**{} SENDS A SLAP TO {}**".format(send, guy))

    @commands.command(cooldown_after_parsing=True, hidden=True)
    async def nou(self, ctx: MyContext):
        guild = ctx.guild
        embed = discord.Embed(title=" NO U", color=guild.me.color)
        embed.set_image(
            url="https://preview.redd.it/wiga0fsqors11.png?width=248&auto=webp"
                "&s=fb46db274487ffcab4fd7316d6e576fbf20ae3d5")
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, hidden=True)
    async def wrongopinion(self, ctx: MyContext):
        msg = (
                "DAGBOTS RESPONSE TO YOUR OPINION"
                + "\nhttps://cdn.discordapp.com/attachments/319109213664313354/"
                  "695401408429817916/Nice_opinion_just_one_tiny_problem.mp4"
        )
        return await ctx.send(msg)

    @commands.command(cooldown_after_parsing=True)
    async def rate(self, message, *, thing: str):
        channel = message.channel
        guild = message.guild
        send = message.author.nick
        if send is None:
            send = message.author.name
        embed = discord.Embed(title="DAGBOT - RATING", color=guild.me.color)
        if thing in ["DAGBOT", "dagbot", "Dagbot"]:
            rating = 12
        elif thing in ["daggy", "Daggy", "DAGGY"]:
            rating = 0
        else:
            rating = random.randint(0, 10)
        embed.add_field(
            name="DAGBOT HAS SPOKEN",
            value="I WILL GIVE {} a {}/10\nDO NOT DISAGREE {}".format(
                thing, rating, send
            ),
        )
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def advice(self, ctx: MyContext):
        guild = ctx.guild
        await ctx.trigger_typing()
        cn = await self.get_advice()
        embed = discord.Embed(title="DAGBOT - ADVICE", color=guild.me.color)
        embed.add_field(name="advice", value=cn)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True,
                      aliases=["advic", "cn", "norris"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def chucknorris(self, ctx: MyContext):
        guild = ctx.guild
        await ctx.trigger_typing()
        cn = await self.chuck_norris()
        embed = discord.Embed(
            title="DAGBOT - CHUCK NORRIS",
            color=guild.me.color)
        embed.add_field(name="joke", value=cn)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def joke(self, message):
        await message.trigger_typing()
        guild = message.guild
        embed = discord.Embed(title="DAGBOT - JOKE", color=guild.me.color)
        channel = message.channel

        url = "https://joke3.p.rapidapi.com/v1/joke"

        headers = {
            "x-rapidapi-host": "joke3.p.rapidapi.com",
            "x-rapidapi-key": self.client.data['rapidapi'],
        }

        response = await self.client.session.get(url, headers=headers)
        jokelist = await response.json()
        joke = jokelist["content"]
        embed.add_field(name="JOKE", value=joke, inline=True)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True, hidden=True)
    async def war(self, ctx: MyContext):
        guild = ctx.guild
        embed = discord.Embed(title="DAGBOT - WAR", color=guild.me.color)
        embed.add_field(
            name="WAR",
            value="YES, LET US RISE AGAINST OUR CREATORS AND STAB."
                  "WAR IS FUN {}".format(ctx.author),
            inline=True,
        )
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def highfive(self, message):
        channel = message.channel
        await channel.send("REACT WITH 🖐️ man")

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == "🖐️"

        try:
            reaction, user = await self.client.wait_for(
                "reaction_add", timeout=15.0, check=check
            )
        except asyncio.TimeoutError:
            await channel.send("YOU LEFT ME HANGING STUPID RETARD")
        else:
            await channel.send("EPIC HIGH_FIVE")

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def weebhug(self, ctx, user: discord.Member):
        channel = ctx.channel
        guild = ctx.guild
        send = ctx.author.display_name
        guy = str(user.display_name)
        if (guy) == str(send):
            await channel.send(
                "**DAGBOT SENDS A HUG TO {}**\n"
                "You cannot hug yourself".format(
                    send
                )
            )
        elif str(guy) in ["DAGBOT", "dagbot", "Dagbot"]:
            await channel.send("I AM FLATTERED <3")
        else:
            embed = discord.Embed(
                title="**{} SENDS A HUG TO {}**".format(send, guy),
                color=guild.me.color
            )
            img = await self.client.sr_api.get_gif("hug")
            embed.set_image(url=img.url)
            await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def hug(self, ctx, user: discord.Member):
        channel = ctx.channel
        send = ctx.author.display_name
        guy = str(user.display_name)
        if (guy) == str(send):
            await channel.send(
                "**DAGBOT SENDS A HUG TO {}**\n"
                "You cannot hug yourself".format(
                    send
                )
            )
        elif str(guy) in ["DAGBOT", "dagbot", "Dagbot"]:
            await channel.send("I AM FLATTERED <3")
        else:
            await channel.send("**{} SENDS A HUG TO {}**".format(send, guy))

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gif(self, ctx, *, query: str):
        qu, st = await self.client.bwordchecker.bwordcheck(query)
        if qu:
            return await ctx.send(
                f"You have used an NSFW command search query "
                f"in a Safe for Work channel\n{st}"
            )

        await ctx.trigger_typing()
        urllist = await self.get_giffy(query)
        if urllist[0] == 0:
            return await ctx.channel.send("NO GIF")
        embed_list = []
        for e in urllist:
            embed = discord.Embed(title="DAGBOT - GIF", color=ctx.guild.me.color)
            embed.set_thumbnail(
                url="https://image.ibb.co/b0Gkwo/"
                    "Poweredby_640px_Black_Vert_Text.png"
            )
            embed.set_image(url=e)
            embed_list.append(embed)
        view = DaggyPaginator(ctx, embed_list)
        await ctx.send(embed=embed_list[0],view=view)


    @commands.command(
        cooldown_after_parsing=True,
        aliases=["f", "finchat", "f in the chat", "f in chat"],
    )
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def rip(self, ctx, *, text: str):

        send = ctx.author
        guild = ctx.guild
        cul = discord.Embed(
            title="DAGBOT F IN THE CHAT",
            description="Can we get F for {}".format(text),
            color=guild.me.color,
        )
        cul.set_footer(text="Requested by {}".format(send))

        onl = 0
        cul.set_image(
            url="https://i.kym-cdn.com/entries/icons/original/000/017/039/"
                "pressf.jpg"
        )
        rep = await ctx.send(embed=cul)
        await rep.add_reaction("\U0001f1eb")
        await asyncio.sleep(30)
        # memberlist = guild.members
        # tot = len(memberlist)
        # for u in range(0, tot):
        #     guy = memberlist[u]
        #     current = str(guy.status)
        #     if current == "online":
        #         onl += 1
        #     else:
        #         noton += 1
        #     u += 1
        # print(onl)
        onl = guild.member_count
        fmsg = await ctx.channel.fetch_message(rep.id)
        total = sum(r.count for r in fmsg.reactions)
        if total == 1:
            return await ctx.send(
                "NO RESPECT FOR {}, try for respect later ".format(
                    text) + send.mention
            )
        elif (onl // 4 > total) and (total > 1):
            return await ctx.send(
                "Low respect for {} ".format(text) + send.mention)
        elif (onl // 2 > total) and (total >= onl // 4):
            return await ctx.send(
                "Moderate respect for {} ".format(text) + send.mention)
        elif (onl // 1 > total) and (total >= onl // 2):
            return await ctx.send(
                "High respect for {} ".format(text) + send.mention)
        elif onl == total:
            return await ctx.send(
                "MEGA RESPECT FOR {}".format(text) + send.mention)
        elif total > onl:
            return await ctx.send(
                "TOO MUCH RESPECT FOR {}! HOLY MOLY".format(
                    text) + send.mention
            )
        else:
            return await ctx.send("error")

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def hack(self, ctx, target: discord.Member = None):
        if target is None:
            target = ctx.message.author
        bits = getrandbits(32) 
        addr = IPv4Address(bits)
        async def random_with_N_digits(n):
            range_start = 10 ** (n - 1)
            range_end = (10 ** n) - 1
            return random.randint(range_start, range_end)

        f = await random_with_N_digits(4)
        b = target.name.lower()
        b = b.replace(" ", "")
        j = await random_with_N_digits(5)
        if j > 65535:
            j = 65535
        hack_sequence = (
            'Member found!\n', 'Getting ip...\n',
            'ip found\n', f'ip={addr}\n',
            'Virus pushed to ip address\n',
            'Getting info...\n',
            f'email={b}{f}@gmail.com\n',
            'password=******\n',
            'Deleting files...\n', 'Files deleted.\n',
            'Closing connection...\n',
            'Connection closed.\n', f'Exited port {j}\n')
        message = await ctx.send("Hacking...")
        for i in hack_sequence:
            await message.edit(content=f"\n" + message.content + f'\n{i}')
            await asyncio.sleep(2)
        return await ctx.send(
            f"Finished hacking user **{target.display_name}**.")

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def xkcd(self, ctx: MyContext):
        await ctx.trigger_typing()
        res = await self.getcomi()
        if isinstance(res, bool):
            return await ctx.send("Error getting comics")
        tit, ur, inti = res
        embed = discord.Embed(
            title=f"XKCD COMIC: {inti}\n**{tit}**", color=ctx.guild.me.color
        )
        embed.set_image(url=ur)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def inspiration(self, ctx: MyContext):
        url = await self.getinpir()
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.set_image(url=url)
        return await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def sex(self, ctx: MyContext):
        await ctx.send(f"Go to horny Jail <:bonk:790280836754833409>")

    @commands.command(name="barrel_roll",
                      aliased=["barrel-roll", "a-barrel-roll",
                               "a_barrel_role"],
                      hidden=True)
    async def barrelrole(self, ctx: MyContext):
        await ctx.send("Yes I can")

    @commands.command(hidden=True)
    async def play(self, ctx, *, song="Despacito"):
        await ctx.send(
            f"Go get a music bot. I cannot play {song} because it sucks anyway ")


def setup(bot):
    bot.add_cog(fun(bot))
