from __future__ import annotations
import functools
from typing import Any, Dict, Tuple, List, Union
from dagbot.bot import Dagbot
from dagbot.utils.context import MyContext
import random

import discord
from bs4 import BeautifulSoup
from discord.ext import commands





async def setup(client):
    await client.add_cog(smart(client))


# return(resp['yodish'])
# async def getyoda(string):
#     url="http://www.yodaspeak.co.uk/webservice/yodatalk.php?wsdl"
# #headers = {'content-type': 'application/soap+xml'}
#     headers = {'content-type': 'text/xml'}
#     body = '''<?xml version="1.0" encoding="ISO-8859-1"?>
# <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" \
# xmlns:yod="uri:http://www.yodaspeak.co.uk/webservice/yodatalk">
#    <soapenv:Header/>
#    <soapenv:Body>
#       <yod:yodaTalk>
#          <inputText>{}</inputText>
#       </yod:yodaTalk>
#    </soapenv:Body>
# </soapenv:Envelope>'''.format(string)
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url,data=body,headers=headers) as response:
#             d = (response.content)
#             html = await d.read()
#             print(html)
#             soup = BeautifulSoup(html,'html.parser')
#             y = (soup.find('return').text)
#             return(y)
class smart(commands.Cog):
    """Nerd commands (be proud)"""

    def __init__(self, client: Dagbot):
        self.client: Dagbot = client

    async def cog_check(self, ctx: MyContext):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                return bool(e["smart"])

    # async def characterhpget(self, y: str) -> Tuple[bool, str]:
    #     response = await self.client.session.get(
    #         f"https://www.potterapi.com/v1/characters?"
    #         f"key={self.client.data['hpapikey']}"
    #     )
    #     flist: Dict[str, Any] = await response.json()
    #     vallist: List[str] = []
    #     for i in range(len(flist)):
    #         dictg = flist[i]
    #         name = dictg.get("name")
    #         if y in name:
    #             vallist.append(str(i))
    #         else:
    #             i += 1
    #     if not vallist:
    #         return False, ""
    #     elif len(vallist) == 1:
    #         return flist[vallist[0]]
    #     else:
    #         charstring = ""
    #         for q in range(len(vallist)):
    #             char = flist[vallist[q]]["name"]
    #             charstring = charstring + "\n" + char
    #             q += 1
    #         return True, charstring

    # async def get_spell(self, y: str) -> Tuple[bool, str]:
    #     response = await self.client.session.get(
    #         f"https://www.potterapi.com/v1/spells?key="
    #         f"{self.client.data['hpapikey']}"
    #     )
    #     flist = await (response.json())
    #     vallist: List[str] = []
    #     for i in range(len(flist)):
    #         dictg = flist[i]
    #         name = dictg.get("spell")
    #         if y in name:
    #             vallist.append(str(i))
    #         else:
    #             i += 1
    #     if not vallist:
    #         return False, ""
    #     elif len(vallist) == 1:
    #         return flist[vallist[0]]
    #     else:
    #         charstring = ""
    #         for q in range(len(vallist)):
    #             char = flist[vallist[q]]["spell"]
    #             charstring = charstring + "\n" + char
    #             q += 1
    #         return True, charstring

    async def getapod(self) -> Dict[str, Any]:
        url = f"https://api.nasa.gov/planetary/apod?" \
              f"api_key={self.client.data['nasaapikey']}"
        y = await self.client.session.get(url)
        js: Dict[str, Any] = await y.json()
        return js

    async def getnpic(self, url) -> Tuple[bool, List[Union[int, str]]]:
        resp = await self.client.session.get(url)
        js = await resp.json()
        data = js['collection']
        if data['metadata']['total_hits'] == 0:
            return False, []
        lik = data['items'][0]
        resul = len(lik)
        return True, [lik, resul]

    async def getyoda(self, string: str) -> str:
        htmlst = string.replace(" ", "%20")
        url = f"http://yoda-api.appspot.com/api/v1/yodish?text={htmlst}"
        r = await self.client.session.get(url)
        resp = await r.json()
        return resp["yodish"]

    @commands.command(cooldown_after_parsing=True)
    async def quote(self, message: MyContext):
        channel = message.channel
        guild = message.guild
        embed = discord.Embed(title="DAGBOT - QUOTE", color=guild.me.color)
        url = "http://www.quotationspage.com/random.php"
        response = await self.client.session.get(url)
        file = response.content
        html = await file.read()
        soup = BeautifulSoup(html, "html.parser")
        bdy = soup.body
        if not bdy:
            return await message.send("Error while processing command")
        quote = str(bdy.find("dt", attrs={"class": "quote"}).text)
        author = str(bdy.find("b").text)
        embed.add_field(
            name="QUOTE", value=("{}\n{}".format(quote, author)), inline=True
        )
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def yoda(self, ctx, *, string: str):
        await ctx.typing()
        guild = ctx.guild
        embed = discord.Embed(title="DAGBOT - YODISH", color=guild.me.color)
        channel = ctx.channel
        y = await self.getyoda(string)
        embed.add_field(name="YODA SAYS", value=y, inline=True)
        await channel.send(embed=embed)

#     @commands.group(invoke_without_command=True)
#     async def hp(self, ctx):
#         return await ctx.send("Please use `hp help` to get started")

#     @hp.command()
#     async def help(self, ctx):
#         return await ctx.send(
#             """`Harry Potter API,
# hp char <character> : gets character information
# hp spell <spell> : gets information about spell    `"""
#         )

#     @hp.command(aliases=["char", "Characters", "Char"])
#     async def character(self, ctx, *, query):
#         y = await self.characterhpget(query)
#         guild = ctx.guild
#         if not y:
#             return await ctx.send(
#                 "no results for {}, The api is case sensitive so do ensure the"
#                 "first letter is Caps".format(
#                     query
#                 )
#             )
#         elif isinstance(y, dict):
#             embed = discord.Embed(
#                 title="DAGBOT - HARRY POTTER  Character RESULTS",
#                 color=guild.me.color
#             )
#             embed.add_field(name="Name", value=y["name"], inline=False)
#             try:
#                 role = y["role"]
#             except BaseException:
#                 pass
#             else:
#                 embed.add_field(name="Role", value=role, inline=False)
#                 if y["role"] == "student":
#                     embed.add_field(name="House", value=y["house"])
#             try:
#                 wand = y["wand"]
#             except BaseException:
#                 pass
#             else:
#                 embed.add_field(name="Wand", value=wand, inline=False)
#             try:
#                 boggart = y["boggart"]
#             except BaseException:
#                 pass
#             else:
#                 embed.add_field(name="Boggart", value=boggart, inline=False)
#             try:
#                 patronus = y["patronus"]
#             except BaseException:
#                 pass
#             else:
#                 embed.add_field(name="Patronus", value=patronus, inline=False)
#             if y["ministryOfMagic"]:
#                 embed.add_field(
#                     name="-",
#                     value="Ministry Of Magic",
#                     inline=True)
#             if y["orderOfThePhoenix"]:
#                 embed.add_field(
#                     name="-",
#                     value="Order Of the Phoenix",
#                     inline=True)
#             if y["dumbledoresArmy"]:
#                 embed.add_field(
#                     name="-",
#                     value="Dumbledores Army",
#                     inline=True)
#             if y["deathEater"]:
#                 embed.add_field(name="-", value="Death Eater", inline=True)
#             embed.add_field(
#                 name="Blood Status",
#                 value=y["bloodStatus"],
#                 inline=False)
#             embed.add_field(name="Species", value=y["species"], inline=False)
#             return await ctx.send(embed=embed)
#         else:
#             embed = discord.Embed(
#                 title="DAGBOT - HARRY POTTER  Characters MULTIPLE RESULTS",
#                 color=guild.me.color,
#             )
#             embed.add_field(name="Results", value=y)
#             embed.add_field(
#                 name="Tip",
#                 value="Please specify/be more detailed")
#             return await ctx.send(embed=embed)

#     @hp.command(aliases=["Spell", "spl", "Spl"])
#     async def spell(self, ctx, *, query):
#         y = self.get_spell(query)
#         guild = ctx.guildß
#         if not y:
#             return await ctx.send(
#                 "no results for {}, The api is case sensitive so do "
#                 "ensure the first letter is Caps".format(
#                     query
#                 )
#             )
#         elif isinstance(y, dict):
#             embed = discord.Embed(
#                 title="DAGBOT - HARRY POTTER SPELL", color=guild.me.color
#             )
#             embed.add_field(name="spell", value=y["spell"])
#             embed.add_field(name="type", value=y["type"])
#             embed.add_field(name="effect", value=y["effect"])
#             return await ctx.send(embed=embed)
#         else:
#             embed = discord.Embed(
#                 title="DAGBOT - HARRY POTTER SPELLS MULTIPLE RESULTS",
#                 color=guild.me.color,
#             )
#             embed.add_field(name="Results", value=y)
#             embed.add_field(
#                 name="Tip",
#                 value="Please specify/be more detailed")
#             return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True,
                      aliases=['astronomy pic of the day'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def apod(self, ctx: MyContext):
        js = await self.getapod()
        embed = discord.Embed(
            title=js['title'],
            description=js['explanation'],
            color=ctx.guild.me.color)

        hd_url = js.get('hdurl')
        if hd_url:
            embed.set_image(url=hd_url)
            return await ctx.send(embed=embed)
        return await ctx.send(str(js.get("url")),embed=embed)
        

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nasapic(self, ctx: MyContext, *, query: str):
        url = f'https://images-api.nasa.gov/search?q={query}'
        resp = await self.getnpic(url)
        if not resp:
            return await ctx.send('No reults for your query')
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.set_image(url=resp[0])
        embed.set_footer(text=f'Returned {resp[1]} results for your query')

    @commands.command(cooldown_after_parsing=True)
    async def oeis(self, ctx: MyContext, num: int = 891):
        if num == 891:
            num = random.randint(1, 299999)
        guild = ctx.guild
        url = f"https://oeis.org/A{num}"
        f = await self.client.session.get(url)
        html = await f.read()

        soup = BeautifulSoup(html, "html.parser")
        intl_f = soup.find("tt")
        iti_f = soup.find("td", align="left")
        if not intl_f or not iti_f:
            return await ctx.send(f"NO RESULTS FOR {num}")

        iti = iti_f.text
        l_dat = iti.replace("\n", "")
        char = 0
        chrli = []
        for i in range(len(l_dat)):
            if l_dat[i] == " " and char == 0:
                chrli.append("")
                char = 0
            elif l_dat[i] == " " and char == 1:
                chrli.append(" ")
                char = 0
            elif l_dat[i] != " ":
                chrli.append(l_dat[i])
                char = 1
            i += 1
        mst = "".join(chrli)
        # print(chrli)
        embed = discord.Embed(
            title=f"`{mst}`", url=url, color=guild.me.color
        )
        embed.add_field(name="LIST", value=intl_f.text)
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def fact(self, message: MyContext):
        await message.trigger_typing()
        channel = message.channel
        guild = message.guild
        url = "https://www.kickassfacts.com/random-facts/"
        r = await self.client.session.get(url)
        html = await r.text()
        fact = []
        factlink = []
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("img"):
            fact.append(link.get("alt"))
            factlink.append(link.get("src"))
        embed = discord.Embed(title="DAGBOT - FUN FACT", color=guild.me.color)
        embed.set_image(url=factlink[3])
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def define(self, ctx: MyContext, *, word: str):
        await ctx.typing()
        fn = functools.partial(self.client.dictionary.meaning, word)
        dict_ =  await self.client.loop.run_in_executor(None, fn)
        if not dict_:
            return await ctx.send("No Definitons")
        k = dict_.keys()
        mast = ""
        for i in k:
            mli = dict_[i]
            mast += f"\n__TYPE__:**{i}**"
            mast += "\n__Meaning:__"
            for e in mli:
                mast += f"\n{e}"
        emed = discord.Embed(
            title=f"**WORD: {word}**",
            description=mast,
            color=ctx.guild.me.color)
        return await ctx.send(embed=emed)

    @commands.command(cooldown_after_parsing=True)
    async def numfact(self, message: MyContext):
        await message.trigger_typing()
        channel = message.channel
        guild = message.guild
        url = "http://numbersapi.com/random/trivia"
        embed = discord.Embed(
            title="DAGBOT - NUMBER FACT",
            color=guild.me.color)
        response = await self.client.session.get(url)
        fact = await response.text()
        embed.add_field(name="NUMBER FACT", value=fact, inline=True)
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def numsearch(self, message: MyContext, *, num: int):
        channel = message.channel
        guild = message.guild
        embed = discord.Embed(
            title="DAGBOT - NUMBER FACT FOR NUMBER", color=guild.me.color
        )
        url = "http://numbersapi.com/{}/math".format(num)
        response = await self.client.session.get(url)
        fact = await response.text()
        embed.add_field(name="NUMBER", value=str(num), inline=True)
        embed.add_field(name="NUMBER FACT", value=fact, inline=False)
        await channel.send(embed=embed)

    # @commands.command(cooldown_after_parsing=True)
    # async def pokedex(self, message: MyContext, *, pokemon: str):

    #     await message.trigger_typing()
    #     channel = message.channel
    #     guild = message.guild
    #     pokemon = str(pokemon)
    #     pokemon = pokemon.lower()
    #     url = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon)
    #     embed = discord.Embed(title="DAGBOT - POKEDEX", color=guild.me.color)
    #     response = await self.client.session.get(url)
    #     try:
    #         file = await response.json()
    #     except BaseException:
    #         embed.add_field(
    #             name="ERROR",
    #             value="POKEMON DOES NOT EXIST ENTER NUMBER/NAME IN ALL SMALLS",
    #             inline=True,
    #         )
    #         await channel.send(embed=embed)

    #     else:
    #         pokemon = file["name"]
    #         embed.add_field(name="POKEMON", value=pokemon, inline=True)
    #         embed.add_field(name="Id", value=file["id"], inline=True)
    #         stat_list = file["stats"]
    #         poke = await (self.get_pokemon(pokemon))
    #         embed.add_field(name="Title", value=poke["Category"], inline=True)
    #         embed.add_field(name="Entry", value=poke["entry"], inline=False)
    #         embed.add_field(name="Height", value=poke["Height"], inline=True)
    #         embed.add_field(name="Weight", value=poke["Weight"], inline=True)
    #         if len(file["types"]) == 1:
    #             embed.add_field(
    #                 name="Type 1",
    #                 value=file["types"][0]["type"]["name"],
    #                 inline=False,
    #             )
    #         else:
    #             embed.add_field(
    #                 name="Type 1",
    #                 value=file["types"][0]["type"]["name"],
    #                 inline=False,
    #             )
    #             embed.add_field(
    #                 name="Type 2",
    #                 value=file["types"][1]["type"]["name"],
    #                 inline=True,
    #             )
    #         embed.set_thumbnail(url=poke["fimage"])
    #         embed.set_thumbnail(url=poke["fimage"])
    #         mstring = ""
    #         for i in range(len(stat_list)):
    #             val = stat_list[i]["base_stat"]
    #             name = stat_list[i]["stat"]["name"]
    #             mstring += "\n{}: {}".format(name, val)
    #             i += 1
    #         embed.add_field(name="STATS", value=mstring, inline=False)
    #         abilitylist = file["abilities"]
    #         mstringyu = ""
    #         for qc in range(len(abilitylist)):
    #             try:
    #                 ablename = abilitylist[qc]["ability"]["name"]
    #                 mstringyu += "\nAbility {}: {}".format(
    #                     qc + 1, ablename
    #                 )
    #             except BaseException:
    #                 pass
    #             qc += 1

    #         embed.add_field(name="abilitylist", value=mstringyu, inline=False)
    #         embed.add_field(
    #             name="Evolutions", value="------------", inline=False
    #         )
    #         for evu in range(len(poke["image"])):
    #             embed.add_field(
    #                 name=poke["id"][evu], value=poke["name"][evu], inline=True
    #             )
    #             evu += 1
    #         embed.set_image(url=poke["fimage"])
    #         await channel.send(embed=embed)
