import random
from contextlib import suppress

import discord
from PyDictionary import PyDictionary
from bs4 import BeautifulSoup
from discord.ext import commands

dictionary = PyDictionary()


def setup(client):
    client.add_cog(smart(client))


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

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(g_id):
                if e["smart"]:
                    return True
                else:
                    return False

    async def characterhpget(self, y):
        response = await self.client.session.get(
            f"https://www.potterapi.com/v1/characters?\
                key={self.client.data['hpapikey']}"
        )
        flist = await (response.json())
        vallist = []
        for i in range(0, len(flist)):
            dictg = flist[i]
            name = dictg.get("name")
            if y in name:
                vallist.append(i)
            else:
                i += 1
        if len(vallist) == 0:
            return False
        elif len(vallist) == 1:
            return flist[vallist[0]]
        else:
            charstring = ""
            for q in range(0, (len(vallist))):
                char = flist[vallist[q]]["name"]
                charstring = charstring + "\n" + char
                q += 1
            return charstring

    async def get_pokemon(self, pokemon):
        pokemon = pokemon.lower()
        response = await self.client.session.get(
            f"https://api.pokemon.com/us/pokedex/{pokemon}"
        )
        d = response.content
        html = await d.read()
        soup = BeautifulSoup(html, "html.parser")
        head = str(
            soup.body.find(
                "div", attrs={
                    "class": "column-12 push-1 dog-ear-bl"})
        )
        pokimg = str(soup.body.find("img", attrs={"class": "active"})["src"])
        evoidlist = []
        evoimg = []
        evoname = []
        evoidf = []
        evonamef = []

        soupa = BeautifulSoup(head, "html.parser")
        for info in soupa.find_all("h3"):
            evoidlist.append(info.find("span").text)
            evoname.append(info.text)
        for link in soupa.find_all("img"):
            evoimg.append(link.get("src"))
        try:
            for i in range(0, len(evoname)):
                _id = evoidlist[i]
                name = evoname[i]
                fid = _id.replace(" ", "")
                fid = fid.replace("\n", "")
                fname = name.replace(" ", "")
                fname = fname.replace("\n", "")
                fname = fname.replace("#", "")
                fname = fname.replace("1", "")
                fname = fname.replace("3", "")
                fname = fname.replace("2", "")
                fname = fname.replace("4", "")
                fname = fname.replace("5", "")
                fname = fname.replace("6", "")
                fname = fname.replace("7", "")
                fname = fname.replace("8", "")
                fname = fname.replace("9", "")
                fname = fname.replace("0", "")
                evoidf.append(fid)
                evonamef.append(fname)
                i += 1
        except KeyError:
            evoidf = ['Error']
            evonamef = ['Error']
        datafact = []
        infobox = str(
            soup.body.find(
                "p", attrs={
                    "class": "version-y active"}).text)
        infobox = infobox.replace("\n", "")

        pokinfo = str(
            soup.body.find(
                "div",
                attrs={
                    "class": "pokemon-ability-info color-bg color-lightblue match active"
                },
            )
        )
        soupb = BeautifulSoup(pokinfo, "html.parser")
        for datainfo in soupb.find_all("span"):
            datafact.append(datainfo.get_text())
        pokedict = {
            "name": evonamef,
            "image": evoimg,
            "id": evoidf,
            "entry": infobox,
            "fimage": pokimg,
        }
        for cul in range(0, len(datafact)):
            with suppress(Exception):
                pokedict[datafact[cul]] = datafact[cul + 1]

            cul += 2
        return pokedict

    async def spell(self, y):
        response = await self.client.session.get(
            f"https://www.potterapi.com/v1/spells?key={self.client.data['hpapikey']}"
        )
        flist = await (response.json())
        vallist = []
        for i in range(0, len(flist)):
            dictg = flist[i]
            name = dictg.get("spell")
            if y in name:
                vallist.append(i)
            else:
                i += 1
        if len(vallist) == 0:
            return False
        elif len(vallist) == 1:
            return flist[vallist[0]]
        else:
            charstring = ""
            for q in range(0, (len(vallist))):
                char = flist[vallist[q]]["spell"]
                charstring = charstring + "\n" + char
                q += 1
            return charstring

    async def getapod(self):
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.client.data['nasaapikey']}"
        y = await self.client.session.get(url)
        js = await y.json()
        return js

    async def getnpic(self, url):
        resp = await self.client.session.get(url)
        js = await resp.json()
        data = js['collection']
        if data['metadata']['total_hits'] == 0:
            return (False)
        else:
            lik = data['items'][0]
            resul = len(lik)
            return ([lik, resul])

    async def getyoda(self, string):
        htmlst = string.replace(" ", "%20")
        url = f"http://yoda-api.appspot.com/api/v1/yodish?text={htmlst}"
        r = await self.client.session.get(url)
        resp = await r.json()
        return resp["yodish"]

    @commands.command(cooldown_after_parsing=True)
    async def quote(self, message):
        channel = message.channel
        guild = message.guild
        embed = discord.Embed(title="DAGBOT - QUOTE", color=guild.me.color)
        url = "http://www.quotationspage.com/random.php"
        response = await self.client.session.get(url)
        file = response.content
        html = await file.read()
        soup = BeautifulSoup(html, "html.parser")
        quote = str(soup.body.find("dt", attrs={"class": "quote"}).text)
        author = str(soup.body.find("b").text)
        embed.add_field(
            name="QUOTE", value=("{}\n{}".format(quote, author)), inline=True
        )
        await channel.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def yoda(self, ctx, *, string: str):
        await ctx.trigger_typing()
        guild = ctx.guild
        embed = discord.Embed(title="DAGBOT - YODISH", color=guild.me.color)
        channel = ctx.channel
        y = await self.getyoda(string)
        embed.add_field(name="YODA SAYS", value=y, inline=True)
        await channel.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def hp(self, ctx):
        return await ctx.send("Please use `hp help` to get started")

    @hp.command()
    async def help(self, ctx):
        return await ctx.send(
            """`Harry Potter API,
hp char <character> : gets character information
hp spell <spell> : gets information about spell    `"""
        )

    @hp.command(aliases=["char", "Characters", "Char"])
    async def character(self, ctx, *, query):
        y = await self.characterhpget(query)
        guild = ctx.guild
        if not y:
            return await ctx.send(
                "no results for {}, The api is case sensitive so do ensure the first letter is Caps".format(
                    query
                )
            )
        elif isinstance(y, dict):
            embed = discord.Embed(
                title="DAGBOT - HARRY POTTER  Character RESULTS",
                color=guild.me.color
            )
            embed.add_field(name="Name", value=y["name"], inline=False)
            try:
                role = y["role"]
            except BaseException:
                i = 1
            else:
                embed.add_field(name="Role", value=role, inline=False)
                if y["role"] == "student":
                    embed.add_field(name="House", value=y["house"])
            try:
                wand = y["wand"]
            except BaseException:
                i = 1
            else:
                embed.add_field(name="Wand", value=wand, inline=False)
            try:
                boggart = y["boggart"]
            except BaseException:
                i = 1
            else:
                embed.add_field(name="Boggart", value=boggart, inline=False)
            try:
                patronus = y["patronus"]
            except BaseException:
                i = 1
            else:
                embed.add_field(name="Patronus", value=patronus, inline=False)
            if y["ministryOfMagic"]:
                embed.add_field(
                    name="-",
                    value="Ministry Of Magic",
                    inline=True)
            if y["orderOfThePhoenix"]:
                embed.add_field(
                    name="-",
                    value="Order Of the Phoenix",
                    inline=True)
            if y["dumbledoresArmy"]:
                embed.add_field(
                    name="-",
                    value="Dumbledores Army",
                    inline=True)
            if y["deathEater"]:
                embed.add_field(name="-", value="Death Eater", inline=True)
            embed.add_field(
                name="Blood Status",
                value=y["bloodStatus"],
                inline=False)
            embed.add_field(name="Species", value=y["species"], inline=False)
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="DAGBOT - HARRY POTTER  Characters MULTIPLE RESULTS",
                color=guild.me.color,
            )
            embed.add_field(name="Results", value=y)
            embed.add_field(
                name="Tip",
                value="Please specify/be more detailed")
            return await ctx.send(embed=embed)

    @hp.command(aliases=["Spell", "spl", "Spl"])
    async def spell(self, ctx, *, query):
        y = self.spell(query)
        guild = ctx.guild
        if not y:
            return await ctx.send(
                "no results for {}, The api is case sensitive so do ensure the first letter is Caps".format(
                    query
                )
            )
        elif isinstance(y, dict):
            embed = discord.Embed(
                title="DAGBOT - HARRY POTTER SPELL", color=guild.me.color
            )
            embed.add_field(name="spell", value=y["spell"])
            embed.add_field(name="type", value=y["type"])
            embed.add_field(name="effect", value=y["effect"])
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="DAGBOT - HARRY POTTER SPELLS MULTIPLE RESULTS",
                color=guild.me.color,
            )
            embed.add_field(name="Results", value=y)
            embed.add_field(
                name="Tip",
                value="Please specify/be more detailed")
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True,
                      aliases=['astronomy pic of the day'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def apod(self, ctx):
        js = await self.getapod()
        embed = discord.Embed(
            title=js['title'],
            description=js['explanation'],
            color=ctx.guild.me.color)
        embed.set_image(url=js['hdurl'])
        return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nasapic(self, ctx, *, query):
        url = f'https://images-api.nasa.gov/search?q={query}'
        resp = await self.getnpic(url)
        if not resp:
            return await ctx.send('No reults for your query')
        else:
            embed = discord.Embed(color=ctx.guild.me.color)
            embed.set_image(url=resp[0])
            embed.set_footer(text=f'Returned {resp[1]} results for your query')

    @commands.command(cooldown_after_parsing=True)
    async def oeis(self, ctx, num: int = 891):
        if num == 891:
            num = random.randint(1, 299999)
        guild = ctx.guild
        url = f"https://oeis.org/A{num}"
        f = await self.client.session.get(url)
        int_ = f.content
        html = await f.read()

        soup = BeautifulSoup(html, "html.parser")
        try:
            intl = soup.find("tt").text
        except BaseException:
            return await ctx.send(f"NO RESULTS FOR {num}")
        else:
            iti = soup.find("td", align="left").text
            l = iti.replace("\n", "")
            char = 0
            chrli = []
            for i in range(0, len(l)):
                if l[i] == " " and char == 0:
                    chrli.append("")
                    char = 0
                elif l[i] == " " and char == 1:
                    chrli.append(" ")
                    char = 0
                elif l[i] != " ":
                    chrli.append(l[i])
                    char = 1
                i += 1
            mst = ""
            for e in chrli:
                mst = mst + e
            # print(chrli)
            embed = discord.Embed(
                title=f"`{mst}`", url=url, color=guild.me.color
            )
            embed.add_field(name="LIST", value=intl)
            return await ctx.send(embed=embed)

    @commands.command(cooldown_after_parsing=True)
    async def fact(self, message):
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
    async def define(self, ctx, *, word: str):
        await ctx.trigger_typing()
        dict_ = dictionary.meaning(word)
        k = dict_.keys()
        mast = ""
        tlist = []
        for i in k:
            mli = dict_[i]
            mast = mast + f"\n__TYPE__:**{i}**"
            mast = mast + f"\n__Meaning:__"
            for e in mli:
                mast = mast + f"\n{e}"
        emed = discord.Embed(
            title=f"**WORD: {word}**",
            description=mast,
            color=ctx.guild.me.color)
        return await ctx.send(embed=emed)

    @commands.command(cooldown_after_parsing=True)
    async def numfact(self, message):
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
    async def numsearch(self, message, *, num: int):
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

    @commands.command(cooldown_after_parsing=True)
    async def pokedex(self, message, *, pokemon):

        await message.trigger_typing()
        channel = message.channel
        guild = message.guild
        pokemon = str(pokemon)
        pokemon = pokemon.lower()
        url = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon)
        embed = discord.Embed(title="DAGBOT - POKEDEX", color=guild.me.color)
        response = await self.client.session.get(url)
        try:
            file = await response.json()
        except BaseException:
            embed.add_field(
                name="ERROR",
                value="POKEMON DOES NOT EXITST ENTER NUMBER/NAME IN ALL SMALLS",
                inline=True,
            )
            await channel.send(embed=embed)

        else:
            pokemon = file["name"]
            embed.add_field(name="POKEMON", value=pokemon, inline=True)
            embed.add_field(name="Id", value=file["id"], inline=True)
            stat_list = file["stats"]
            poke = await (self.get_pokemon(pokemon))
            embed.add_field(name="Title", value=poke["Category"], inline=True)
            embed.add_field(name="Entry", value=poke["entry"], inline=False)
            embed.add_field(name="Height", value=poke["Height"], inline=True)
            embed.add_field(name="Weight", value=poke["Weight"], inline=True)
            if len(file["types"]) == 1:
                embed.add_field(
                    name="Type 1",
                    value=file["types"][0]["type"]["name"],
                    inline=False,
                )
            else:
                embed.add_field(
                    name="Type 1",
                    value=file["types"][0]["type"]["name"],
                    inline=False,
                )
                embed.add_field(
                    name="Type 2",
                    value=file["types"][1]["type"]["name"],
                    inline=True,
                )
            embed.set_thumbnail(url=poke["fimage"])
            embed.set_thumbnail(url=poke["fimage"])
            mstring = ""
            for i in range(0, len(stat_list)):
                val = stat_list[i]["base_stat"]
                name = stat_list[i]["stat"]["name"]
                mstring = mstring + "\n{}: {}".format(name, val)
                i += 1
            embed.add_field(name="STATS", value=mstring, inline=False)
            abilitylist = file["abilities"]
            mstringyu = ""
            for qc in range(0, (len(abilitylist))):
                try:
                    ablename = abilitylist[qc]["ability"]["name"]
                    mstringyu = mstringyu + "\nAbility {}: {}".format(
                        qc + 1, ablename
                    )
                except BaseException:
                    tfdtfdtefdetdfetdfetd = 0
                qc += 1

            embed.add_field(name="abilitylist", value=mstringyu, inline=False)
            embed.add_field(
                name="Evolutions", value="------------", inline=False
            )
            for evu in range(0, len(poke["image"])):
                embed.add_field(
                    name=poke["id"][evu], value=poke["name"][evu], inline=True
                )
                evu += 1
            embed.set_image(url=poke["fimage"])
            await channel.send(embed=embed)
