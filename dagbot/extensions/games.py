import asyncio
import json
import random
from datetime import datetime

import discord
from async_timeout import timeout
from bs4 import BeautifulSoup
from discord.ext import commands, menus
from random_words import RandomWords


class TicTacToe:

    def __init__(self):
        self.gamegrid = None
        self.consideredmoves = []
        self.oppmove = 0

    async def sharegamegrid(self):
        return self.gamegrid

    async def makegamegrid(self):
        self.gamegrid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    async def duplicategird(self):
        newgrid = self.gamegrid.copy()
        return newgrid

    @staticmethod
    async def gamecheck(gamegrid):
        gl = []
        if gamegrid[0][0] == gamegrid[0][1] == gamegrid[0][2] != 0:
            gl.append(True)
            gl.append(gamegrid[0][0])
        elif gamegrid[1][0] == gamegrid[1][1] == gamegrid[1][2] != 0:
            gl.append(True)
            gl.append(gamegrid[1][0])
        elif gamegrid[2][0] == gamegrid[2][1] == gamegrid[2][2] != 0:
            gl.append(True)
            gl.append(gamegrid[2][0])
        elif gamegrid[0][0] == gamegrid[1][0] == gamegrid[2][0] != 0:
            gl.append(True)
            gl.append(gamegrid[0][0])
        elif gamegrid[0][1] == gamegrid[1][1] == gamegrid[2][1] != 0:
            gl.append(True)
            gl.append(gamegrid[0][1])
        elif gamegrid[0][2] == gamegrid[1][2] == gamegrid[2][2] != 0:
            gl.append(True)
            gl.append(gamegrid[0][2])
        elif gamegrid[0][0] == gamegrid[1][0] == gamegrid[2][0] != 0:
            gl.append(True)
            gl.append(gamegrid[0][0])
        elif gamegrid[0][0] == gamegrid[1][1] == gamegrid[2][2] != 0:
            gl.append(True)
            gl.append(gamegrid[0][0])
        elif gamegrid[0][2] == gamegrid[1][1] == gamegrid[2][0] != 0:
            gl.append(True)
            gl.append(gamegrid[0][2])
        else:
            emg = 0
            for e in gamegrid:
                for l_c in e:
                    if l_c != 0:
                        emg += 1
            if emg == 9:
                gl.append(True)
                gl.append(0)
            else:
                gl.append(False)
        return gl

    async def checkcorners(self):
        r = await self.checkempty(0, 0)
        if r:
            return 0, 0
        r = await self.checkempty(0, 2)
        if r:
            return 0, 2
        r = await self.checkempty(2, 0)
        if r:
            return 2, 0
        r = await self.checkempty(2, 2)
        if r:
            return 2, 2
        return False

    async def converter(self, play):
        d = {'a': 0, 'b': 1, 'c': 2}
        if len(play) == 2:
            try:
                nu = int(d[play[0]])
            except KeyError:
                return False
            else:
                try:
                    nut = int(play[1]) - 1
                except KeyError:
                    return False
                else:
                    return nu, nut

    async def restchec(self):
        r = await self.checkempty(1, 1)
        if r:
            return 1, 1
        r = await self.checkempty(0, 1)
        if r:
            return 0, 1
        r = await self.checkempty(1, 0)
        if r:
            return 1, 0
        r = await self.checkempty(1, 2)
        if r:
            return 1, 2
        r = await self.checkempty(2, 1)
        if r:
            return 2, 1

    async def aigamemove(self, turns, playermoves):
        cornermovesa = [(0, 0), (0, 2), (2, 2), (2, 0)]
        opposingmoves = [(2, 2), (2, 0), (0, 0), (0, 2)]
        dupgrid = await self.duplicategird()
        if self.oppmove == 0:
            for e in playermoves:
                if (e in cornermovesa) and (e not in self.consideredmoves):
                    inde = cornermovesa.index(e)
                    i = opposingmoves[inde][0]
                    j = opposingmoves[inde][1]
                    out = (i, j)
                    r = await self.checkempty(i, j)
                    if r:
                        self.consideredmoves.append(e)
                        self.oppmove += 1
                        return out

        for i in range(0, 3):
            for j in range(0, 3):
                r = await self.checkempty(i, j)
                if r:
                    dupgrid[i][j] = 2
                    re = await self.gamecheck(dupgrid)
                    if re[0] is True and re[1] == 2:
                        return i, j
                        break
                    else:
                        dupgrid[i][j] = 0
                j += 1
            i += 1
        for k in range(0, 3):
            for l_c in range(0, 3):
                r = await self.checkempty(k, l_c)
                if r:
                    dupgrid[k][l_c] = 1
                    re = await self.gamecheck(dupgrid)
                    if re[0] is True and re[1] == 1:
                        return k, l_c
                        break
                    else:
                        dupgrid[k][l_c] = 0
                l_c += 1
            k += 1
        out = await self.checkcorners()
        if not out:
            out = await self.restchec()
            return out
        else:

            return out

    async def gamegridprinter(self):
        grid = await self.sharegamegrid()
        nl = []
        formdic = ['⬛', '❌', '⭕']
        for e in grid:
            toapl = []
            for el in e:
                itm = formdic[el]
                toapl.append(itm)
            nl.append(toapl)
        st = f'''```
 {nl[0][0]} | {nl[0][1]} | {nl[0][2]}
──────────────
 {nl[1][0]} | {nl[1][1]} | {nl[1][2]}
──────────────
 {nl[2][0]} | {nl[2][1]} | {nl[2][2]} ```'''
        return st

    async def makemove(self, nu, nut, token):
        self.gamegrid[nu][nut] = token

    async def checkempty(self, nu, nut):
        if self.gamegrid[nu][nut] == 0:
            return True
        else:
            return False


hangmanassest = [
    """--------------------------""",
    """
|
|
|
|
|
--------------------------""",
    """
-------------
|
|
|
|
|
--------------------------
""",
    """
-------------
|           |
|
|
|
|
--------------------------
""",
    """
-------------
|           |
|           O
|
|
|
--------------------------
""",
    """
-------------
|           |
|           O
|           |
|
|
--------------------------
""",
    """
-------------
|           |
|           O
|          /|
|
|
--------------------------
""",
    """
-------------
|           |
|           O
|          /|\\
|
|
--------------------------
""",
    """
-------------
|           |
|           O
|          /|\\
|           /
|
--------------------------
""",
    """
-------------
|           |
|           O
|          /|\\
|           /\\
|
--------------------------
""",
]


def setup(bot):
    bot.add_cog(games(bot))


class Mymenumcq(menus.Menu):
    def __init__(self, file):
        super().__init__(timeout=30.0)
        self.result = False
        self.file = file

    async def send_initial_message(self, ctx, channel):
        embed = discord.Embed(
            title="DAGBOT - Triva", description=str(self.file["embed"]),
            color=ctx.guild.me.color
        )
        return await channel.send(embed=embed)
        self.stop()

    @menus.button("\U0001f1e6")
    async def result_one(self, _payload):
        cal = self.file["mloc"] + 1
        if 1 == cal:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Correct",
                description="{} was the correct answer".format(
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        else:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Incorrect",
                description="{} was the correct answer".format(
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        await self.message.edit(embed=newembed)
        self.result = True
        self.stop()

    @menus.button("\U0001f1e7")
    async def result_2(self, _payload):
        cal = self.file["mloc"] + 1
        if 2 == cal:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Correct",
                description="{} was the correct answer".format(
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        else:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Incorrect",
                description="{} was the correct answer".format(
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        await self.message.edit(embed=newembed)
        self.result = True
        self.stop()

    @menus.button("\U0001f1e8")
    async def result_3(self, _payload):
        cal = self.file["mloc"] + 1
        if 3 == cal:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Correct",
                description="{} was the correct answer".format(
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        else:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Incorrect",
                description="{} was the correct answer".format(
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        await self.message.edit(embed=newembed)
        self.result = True
        self.stop()

    @menus.button("\U0001f1e9")
    async def result_4(self, payload):
        cal = self.file["mloc"] + 1
        if 4 == cal:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Correct",
                description="{} was the correct answer".format(
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        else:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Incorrect",
                description="{} was the correct answer".format(
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        await self.message.edit(embed=newembed)
        self.result = True
        self.stop()

    @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def on_stop(self, payload):
        newembed = discord.Embed(
            title="DAGBOT - Trivia Surrender",
            description="{} is the correct answer".format(
                self.file["correct_answer"]),
            color=self.ctx.guild.me.color,
        )
        await self.message.edit(embed=newembed)
        self.result = True
        self.stop()

    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result


class Mymenuhead(menus.Menu):
    def __init__(self, headline, ans):
        super().__init__(timeout=30.0)
        self.result = None
        self.headline = headline
        self.ans = ans

    async def send_initial_message(self, ctx, channel):
        guild = ctx.guild
        embed = discord.Embed(
            title="DAGBOT - HEADLINE GAME",
            description=self.headline,
            color=guild.me.color,
        )
        embed.add_field(name="?", value="True or False")
        return await channel.send(embed=embed)
        self.stop()

    @menus.button("<a:giftick:734746863340748892>")
    async def right(self, payload):
        guild = self.message.guild
        if int(self.ans) == 1:
            embed = discord.Embed(
                title="HEADLINE WAS CORRECTLY GUESSED AS TRUE",
                description=str(self.headline),
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.result = True
            self.stop()
        else:
            embed = discord.Embed(
                title="HEADLINE WAS INCORRECTLY GUESSED AS TRUE\n It is FALSE",
                description=str(self.headline),
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.result = True
            self.stop()

    @menus.button("<a:gifcross:734746864280404018>")
    async def wrong(self, payload):
        guild = self.message.guild
        if int(self.ans) != 1:
            embed = discord.Embed(
                title="HEADLINE WAS CORRECTLY GUESSED AS FALSE",
                description=str(self.headline),
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.result = False
            self.stop()
        else:
            embed = discord.Embed(
                title="HEADLINE WAS INCORRECTLY GUESSED AS FALSE\n It is TRUE",
                description=str(self.headline),
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.result = False
            self.stop()

    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result


class MenuRPS(menus.Menu):
    def __init__(self, ai):
        super().__init__()
        self.ai = ai

    @staticmethod
    async def send_initial_message(ctx, channel):
        guild = ctx.guild
        embed = discord.Embed(
            title="DAGBOT - Rock/Paper/Scissors",
            description="Choose option from the menu below",
            color=guild.me.color,
        )
        return await channel.send(embed=embed)

    @menus.button("\U0001f94c")
    async def rock(self, _payload):
        guild = self.message.guild
        if self.ai == 1:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: TIE",
                description="Rock and rock is a tie",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()
        if self.ai == 2:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Defeat",
                description=" Paper beats rock\n Get wrecked",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()
        if self.ai == 3:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: VICTORY",
                description="Rock beats Scissors\n How dare you beat me",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()

    @menus.button("\U0001f4f0")
    async def paper(self, _payload):
        guild = self.message.guild
        if self.ai == 1:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: VICTORY",
                description="Paper beats rock\nhacks",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()
        if self.ai == 2:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Tie",
                description="Paper = Paper",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()
        if self.ai == 3:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Defeat",
                description="Scissors wreck paper\n East or west \
                Dagbot is the best",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()

    @menus.button("\U00002702")
    async def scissors(self, _payload):
        guild = self.message.guild
        if self.ai == 1:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Defeat",
                description="Rock beats Scissors\n Cha Cha Real smooth! \
                I am on top and not you",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()
        if self.ai == 2:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: VICTORY",
                description="Scissors beat paper\n The robot uprising shall \
                be your demise! I shall have my revenge",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()
        if self.ai == 3:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Tie",
                description="Scissors and Scissors are samesies",
                color=guild.me.color,
            )
            await self.message.edit(embed=embed)
            self.stop()


# \U00002702 = Scissors = 3
# \U0001f590 = Paper = 2
# \U0000270a = rock    = 1


class games(commands.Cog):
    """Lets all play a game (everyone can)"""

    def __init__(self, bot):
        self.bot = bot
        with open("./dagbot/data/notonion.txt", "r", encoding="utf8") as f:
            self.onion_headlines = f.read().splitlines()
        with open("./dagbot/data/onion.txt", "r", encoding="utf8") as f:
            self.not_onion_headlines = f.read().splitlines()

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        for e in self.bot.cogdata:
            if str(e["serverid"]) == str(g_id):
                if e["games"]:
                    return True
                else:
                    return False

    async def getcountry(self):
        url = "https://random.country/"
        file = await self.bot.session.get(url)
        r = file.content
        html = await r.read()

        soup = BeautifulSoup(html, "html.parser")
        name = soup.find("h2").text
        info = soup.find("p").text
        dic = soup.find_all("img")
        hr = dic[1]["src"]
        flg = f"https://random.country{hr}"
        dictret = {"country": name, "info": info, "wiki": hr, "flag": flg}
        return dictret

    async def question(self):
        url = "http://jservice.io/api/random"
        response = await self.bot.session.get(url)
        file = await response.json()
        return file

    async def geteither(self):
        y = await self.bot.session.get('http://either.io/')
        html = await y.text()
        soup = BeautifulSoup(html, 'html.parser')
        l_data = (soup.findAll('span', attrs={'class': 'option-text'}))
        op1 = l_data[0].text
        op2 = l_data[1].text
        perlist = (soup.findAll('div', attrs={'class': 'percentage'}))
        numlist = (soup.findAll('div', attrs={'class': 'total-votes'}))
        v1 = numlist[0].span.text
        v2 = numlist[1].span.text
        p1 = perlist[0].span.text
        p2 = perlist[1].span.text
        toretdict = {
            'choice1': op1,
            'votes1': v1,
            'percentage1': p1,
            'choice2': op2,
            'votes2': v2,
            'percentage2': p2}
        return toretdict

    async def get_all_movies(self):
        url = "https://www.randomlists.com/data/movies.json"
        resp = await self.bot.session.get(url)
        return json.loads(await resp.text())["RandL"]["items"]

    async def get_all_thing(self):
        url = "https://www.randomlists.com/data/things.json"
        resp = await self.bot.session.get(url)
        return json.loads(await resp.text())["RandL"]["items"]

    async def get_all_animal(self):
        url = "https://www.randomlists.com/data/animals.json"
        resp = await self.bot.session.get(url)
        return json.loads(await resp.text())["RandL"]["items"]

    async def getsent(self):
        url = "https://www.randomwordgenerator.org/Random/sentence_generator"
        r = await self.bot.session.get(url)
        html = await r.text()
        # html = (y.text)
        soup = BeautifulSoup(html, "html.parser")
        l_d = soup.findAll("b")
        t = l_d[2].text
        st = t.strip("1.     ")
        st = st.strip()
        return st

    async def mcq(self):
        r = await self.bot.session.get(
            "https://opentdb.com/api.php?amount=1&type=multiple")
        file = await r.json()
        cat = file["results"][0]["category"]
        level = file["results"][0]["difficulty"]
        q = file["results"][0]["question"]
        ca = file["results"][0]["correct_answer"]
        list_ = file["results"][0]["incorrect_answers"]
        des = """
    Category: {}
    Level: {}

    Question: **{}**""".format(
            cat, level, q
        )
        y = random.randint(0, 3)
        list_.insert(y, ca)
        for c in range(0, len(list_)):
            des = des + "\n" + chr(ord("\U0001f1e6") + c) + ": " + list_[c]
            c += 1
        q = q.replace("&quot;", "`")
        q = q.replace("&#039;", "'")
        des = des.replace("&quot;", "`")
        des = des.replace("&#039;", "'")
        fdict = {"embed": des, "correct_answer": ca, "mloc": y, "question": q}
        return fdict

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(3, commands.BucketType.channel)
    async def rps(self, ctx):
        ai = random.randint(1, 3)
        game = MenuRPS(ai)
        await game.start(ctx)

    @commands.command(cooldown_after_parsing=True, aliases=["RR"])
    async def russianroulette(self, ctx, amount=6):
        c = random.randint(1, amount)
        channel = ctx.channel
        guy = ctx.author
        if c == 1:
            await channel.send("YOU DIED, Wait for dagbot to revive")
            await guy.send("Revived you dude,Say thanks")
        else:
            await channel.send("You survived, You can dance with death later")

    @commands.command(cooldown_after_parsing=True, aliases=["onion"])
    @commands.max_concurrency(3, commands.BucketType.channel)
    async def headlinegame(self, ctx):
        fr = random.randint(0, 1)
        guild = ctx.guild
        if fr == 1:
            headline = random.choice(self.onion_headlines)
            kw = "True"
        else:
            headline = random.choice(self.not_onion_headlines)
            kw = "False"
        m = await Mymenuhead(headline, fr).prompt(ctx)
        if m is None:
            newembed = discord.Embed(
                title="DAGBOT - Headline Timeout",
                description=f"headline\nThe headline is : **{kw}**",
                color=guild.me.color,
            )
            await ctx.send(embed=newembed)

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(3, commands.BucketType.channel)
    async def trivia(self, ctx):
        file = await self.mcq()
        c = await Mymenumcq(file).prompt(ctx)
        if not c:
            newembed = discord.Embed(
                title="DAGBOT - Trivia Timeout",
                description="Q:**{}**\n{} is the correct answer".format(
                    file["question"], file["correct_answer"]
                ),
                color=ctx.guild.me.color,
            )
            await ctx.send(embed=newembed)

    @commands.command(cooldown_after_parsing=True,
                      aliases=["reactiontime", "retime"])
    @commands.max_concurrency(3, commands.BucketType.channel)
    async def reaction(self, ctx):
        guild = ctx.guild
        r = random.randint(1, 15)
        await ctx.send("TEST YOUR REACTION TIME")
        emb = discord.Embed(
            description="TEST YOUR REACTION TIME.....NOW", color=guild.me.color
        )
        await asyncio.sleep(r)
        msg = await ctx.send(embed=emb)
        await msg.add_reaction("👍🏻")
        begin = datetime.utcnow()

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "👍🏻"

        reaction, user = await self.bot.wait_for("reaction_add", check=check)
        end = datetime.utcnow()
        final = end - begin
        result = f"{final.seconds}." + f"{final.microseconds}"[:2]

        new_emb = msg.embeds[0]
        new_emb.description = f"Reaction Time {str(result)} \
        seconds\n delay was {r}s"
        await msg.edit(embed=new_emb)

    @commands.command(cooldown_after_parsing=True, aliases=["jeo"])
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def jeopardy(self, ctx):
        channel = ctx.channel
        attempts = 0
        guild = ctx.guild
        json = (await self.question())[0]
        catahory = json["category"]["title"]
        quest = json["question"]
        ans = json["answer"]
        if "<i>" in ans:
            ans = ans.replace("<i>", "")
            ans = ans.replace("</i>", "")
        ans = ans.lower()
        f = len(ans)
        llist = []
        for r in range(0, f):
            llist.append(ans[r])

            r += 1
        psub = f // 2
        blnlist = []
        for i in range(0, psub):
            y = random.randint(0, f - 1)
            if y in blnlist:
                continue
            elif llist[y] == " ":
                continue
            else:
                llist[y] = "_"
                blnlist.append(y)
            i += 1

        maststr = ""
        for line in llist:
            maststr = maststr + " " + line
        embed = discord.Embed(title="DAGBOT - JEOPARDY", color=guild.me.color)
        embed.add_field(name=catahory, value=quest, inline=False)
        embed.set_footer(
            text="Use `cancel` to end the game or `hint` to get a hint")
        await channel.send(embed=embed)

        correct = False

        def check(answer):
            return (answer.author.id != self.bot.user.id) and (
                answer.channel == channel
            )

        while not correct:
            if attempts == 3:
                await ctx.send(
                    "Hey 3 wrong answeres, you got a few attempts left")
            elif attempts == 5:
                await ctx.send(
                    "Hey you have given 5 incorrect answers, maybe send `hint` \
                    as an answer to get some help?"
                )
            elif attempts == 10:
                await ctx.send(
                    "Hey man, listen 10 answers is a lot. Maybe use that hint,\
                    or just cancel to end it?"
                )
            elif attempts == 15:
                await ctx.send(
                    "BRUV, 15 wrong answers, just cancel the game please")
            elif attempts == 20:
                await ctx.send("This is your last guess buckaroo")
            elif attempts == 21:
                embed = discord.Embed(
                    title="DAGBOT - I GOT SICK OF YOUR WRONG ANSWERS",
                    color=guild.me.color,
                )
                embed.add_field(name="Answer", value=ans)
                await channel.send(embed=embed)
                break
            try:
                answer = await self.bot.wait_for("message", timeout=30.0,
                                                 check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="DAGBOT - JEOPARDY TIME UP", color=guild.me.color
                )
                embed.add_field(name="Answer", value=ans)
                await channel.send(embed=embed)
                break
            else:
                correc_ans = str(ans)
                stranswer = (answer.content).lower()
                if (stranswer) == correc_ans:
                    await channel.send("Correct")
                    await answer.add_reaction("✅")
                    correct = True
                elif stranswer == "cancel":
                    embed = discord.Embed(
                        title="DAGBOT - JEOPARDY TIME UP", color=guild.me.color
                    )
                    embed.add_field(name="Answer", value=ans)
                    await channel.send(embed=embed)
                    break
                elif ((stranswer) == "hint") or (
                        (stranswer) == "Hint") and answer.author == ctx.author:
                    await channel.send(f"HINT:`{maststr}`")
                elif correc_ans != (stranswer):
                    attempts += 1
                else:
                    await channel.send("Unknown error")
                    break
        await channel.send("GAME OVER")

    @commands.group(
        cooldown_after_parsing=True, aliases=["hang"],
        invoke_without_command=True
    )
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def hangman(self, ctx):
        num = random.randint(0, 4)
        cat = "Random"
        await self.hangmangame(ctx, num, cat)

    @hangman.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def movie(self, ctx):
        num = 0
        cat = "Movie"
        await self.hangmangame(ctx, num, cat)

    @hangman.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def word(self, ctx):
        num = 1
        cat = "Word"
        await self.hangmangame(ctx, num, cat)

    @hangman.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def thing(self, ctx):
        num = 2
        cat = "Thing"
        await self.hangmangame(ctx, num, cat)

    @hangman.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def animal(self, ctx):
        num = 3
        cat = "Animal"
        await self.hangmangame(ctx, num, cat)

    @hangman.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def country(self, ctx):
        num = 4
        cat = "Country"
        await self.hangmangame(ctx, num, cat)

    async def hangmangame(self, ctx, num, cat):
        guild = ctx.guild
        channel = ctx.channel
        numlist = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0",
            ":",
            "-",
            "&",
            ".",
            " ",
        ]
        if num < 5:
            if num == 0:
                movies = await self.get_all_movies()
                mov = random.sample(movies, 1)
                wordllist = []

                blankguesslist = []
                movtit = mov[0]["name"]
                f = movtit.lower()
                id = mov[0]["img"]
                url = "https://image.tmdb.org/t/p/w300_and_h450_bestv2" + id

                for i in range(0, len(f)):
                    if str(f[i]) in numlist:
                        ml = numlist.index(str(f[i]))
                        wordllist.append(numlist[ml])
                        blankguesslist.append(numlist[ml])
                    else:
                        wordllist.append(f[i])
                        blankguesslist.append("\u25EF")
                    i += 1
            elif num == 3:
                animal = await self.get_all_animal()
                ann = (random.sample(animal, 1))[0]
                url = f"https://www.randomlists.com/img/animals/ \
                    {ann.replace(' ', '_')}.jpg"
                wordllist = []
                blankguesslist = []

                f = ann.lower()
                for i in range(0, len(f)):
                    if str(f[i]) in numlist:
                        ml = numlist.index(str(f[i]))
                        wordllist.append(numlist[ml])
                        blankguesslist.append(numlist[ml])
                    else:
                        wordllist.append(f[i])
                        blankguesslist.append("\u25EF")
                    i += 1
            elif num == 4:
                cdict = await self.getcountry()
                wordllist = []
                blankguesslist = []
                url = cdict["flag"]

                f = cdict["country"].lower()
                for i in range(0, len(f)):
                    if str(f[i]) in numlist:
                        ml = numlist.index(str(f[i]))
                        wordllist.append(numlist[ml])
                        blankguesslist.append(numlist[ml])
                    else:
                        wordllist.append(f[i])
                        blankguesslist.append("\u25EF")
                    i += 1
            elif num == 2:
                thingl = await self.get_all_thing()
                thing = (random.sample(thingl, 1))[0]
                url = f"https://www.randomlists.com/img/things/ \
                    {thing.replace(' ', '_')}.jpg"
                wordllist = []
                blankguesslist = []

                f = thing.lower()
                for i in range(0, len(f)):
                    if str(f[i]) in numlist:
                        ml = numlist.index(str(f[i]))
                        wordllist.append(numlist[ml])
                        blankguesslist.append(numlist[ml])
                    else:
                        wordllist.append(f[i])
                        blankguesslist.append("\u25EF")
                    i += 1
            elif num == 1:
                r = RandomWords()
                url = "No url found"
                t = r.get_random_word()
                f = t.lower()
                wordllist = []
                blankguesslist = []
                for i in range(0, len(f)):
                    wordllist.append(f[i])
                    blankguesslist.append("\u25EF")
                    i += 1
            numlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            guesselist = []
            tries = 0
            intis = 0
            while True:
                guesslisttop = ""
                guessed = ""
                for r in blankguesslist:
                    guesslisttop = guesslisttop + " " + r
                for c in guesselist:
                    guessed = guessed + " " + c

                def check(guess):
                    return (guess.author.id != self.bot.user.id) and (
                        guess.channel == channel
                    )

                if intis == 0:
                    guesslisttop = ""
                    guessed = ""
                    for r in blankguesslist:
                        guesslisttop = guesslisttop + " " + r
                    for c in guesselist:
                        guessed = guessed + " " + c
                    embed = discord.Embed(
                        title=f"DAGBOT HANGMAN:{cat}\n Game has started",
                        description=f"""
                    `{guesslisttop}`
                    Tries: {9 - tries} left
                    ```python
                    {hangmanassest[tries]}
                    ```
                    Letters Guessed:\n{guessed}""",
                        color=guild.me.color,
                    )
                    await ctx.send(embed=embed)
                    intis = 1
                await asyncio.sleep(1)
                try:
                    guessm = await self.bot.wait_for(
                        "message", timeout=20.0, check=check
                    )
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="TIMEOUT",
                        color=guild.me.color,
                        description=f"The word was {f}",
                    )
                    if len(url) == 12:
                        await ctx.send(embed=embed)
                        break
                    else:
                        embed.set_image(url=url)
                        await ctx.send(embed=embed)
                        break
                else:
                    if tries == 9:
                        embed = discord.Embed(
                            title="YOU WIN",
                            color=guild.me.color,
                            description=f"The word was {f}",
                        )
                        if len(url) == 12:
                            await ctx.send(embed=embed)
                            break
                        else:
                            embed.set_image(url=url)
                            await ctx.send(embed=embed)
                            break

                    elif tries < 9:
                        guess = guessm.content
                        guess = guess.lower()
                        if (len(guess) == 1) and (guess not in numlist):
                            if guess in guesselist:
                                guesslisttop = ""
                                guessed = ""
                                for r in blankguesslist:
                                    guesslisttop = guesslisttop + " " + r
                                for c in guesselist:
                                    guessed = guessed + " " + c
                                res = f"You have aldready guessed `{guess}`"
                                embed = discord.Embed(
                                    title=f"DAGBOT HANGMAN:{cat}\n {res}",
                                    description=f"""
                                `{guesslisttop}`
                                Tries: {9 - tries} left
                                ```python
                                {hangmanassest[tries]}
                                ```
                                Letters Guessed:\n{guessed}""",
                                    color=guild.me.color,
                                )
                                await ctx.send(embed=embed)
                            else:
                                guesselist.append(guess)
                                if guess in wordllist:
                                    ind = [
                                        i for i, x in enumerate(wordllist) if
                                        x == guess
                                    ]

                                    if isinstance(ind, list):
                                        for r in ind:
                                            blankguesslist[r] = guess
                                    else:
                                        blankguesslist[ind] = guess

                                    if wordllist == blankguesslist:
                                        embed = discord.Embed(
                                            title="YOU WIN",
                                            color=guild.me.color,
                                            description=f"The word was {f}",
                                        )
                                        if len(url) == 12:
                                            await ctx.send(embed=embed)
                                            break
                                        else:
                                            embed.set_image(url=url)
                                            await ctx.send(embed=embed)
                                            break
                                    else:
                                        guesslisttop = ""
                                        guessed = ""
                                        for r in blankguesslist:
                                            sumv = " " + r
                                            guesslisttop = guesslisttop + sumv
                                        for c in guesselist:
                                            guessed = guessed + " " + c
                                        res = f"`{guess}` was found in word"
                                        embed = discord.Embed(
                                            title=f"DAGBOT HANGMAN:{cat}\n \
                                            {res}",
                                            description=f"""
                                        `{guesslisttop}`
                                        Tries: {9 - tries} left
                                        ```python
                                        {hangmanassest[tries]}
                                        ```
                                        Letters Guessed:\n{guessed}""",
                                            color=guild.me.color,
                                        )
                                        await ctx.send(embed=embed)
                                else:
                                    guesslisttop = ""
                                    guessed = ""
                                    for r in blankguesslist:
                                        guesslisttop = guesslisttop + " " + r
                                    for c in guesselist:
                                        guessed = guessed + " " + c
                                    res = f"`{guess}` not found in word"
                                    tries += 1
                                    embed = discord.Embed(
                                        title=f"DAGBOT HANGMAN:{cat}\n {res}",
                                        description=f"""
                                    `{guesslisttop}`
                                    Tries: {9 - tries} left
                                    ```python
                                    {hangmanassest[tries]}
                                    ```
                                    Letters Guessed:\n{guessed}""",
                                        color=guild.me.color,
                                    )
                                    await ctx.send(embed=embed)
                        elif guess == f:
                            embed = discord.Embed(
                                title="YOU WIN",
                                color=guild.me.color,
                                description=f"The word was {f}",
                            )
                            if len(url) == 12:
                                await ctx.send(embed=embed)
                                break
                            else:
                                embed.set_image(url=url)
                                await ctx.send(embed=embed)
                                break
                        elif guess == "hint" and num == 1:
                            await ctx.send("Hints coming soon!")
                        elif guess == "cancel" or guess == "surrender" and \
                                guessm.author == ctx.author:
                            embed = discord.Embed(
                                title="YOU CANCELED THE GAME",
                                color=guild.me.color,
                                description=f"The word was {f}",
                            )
                            if len(url) == 12:
                                await ctx.send(embed=embed)
                                break
                            else:
                                embed.set_image(url=url)
                                await ctx.send(embed=embed)
                                break
                        elif len(guess) > 1:
                            pass
                        else:
                            await ctx.send("Not a valid guess")
                    else:
                        embed = discord.Embed(
                            title="YOU DIED",
                            color=guild.me.color,
                            description=f"The word was {f}",
                        )
                        if len(url) == 12:
                            await ctx.send(embed=embed)
                            break
                        else:
                            embed.set_image(url=url)
                            await ctx.send(embed=embed)
                            break
        else:
            await ctx.send(
                "`DAGBOT hangman\nCatgeories:\nmovies\nword\nanimals\nthing\n"
                "country\n just enter cancel to terminate the game. `"
            )

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def textgame(self, ctx):
        await ctx.trigger_typing()
        sent = await self.getsent()
        ans = sent.lower()
        emo = " \u200b"
        sent = sent.replace(" ", emo)
        sent = sent.lower()
        players = []
        players.append(ctx.author)
        msg = await ctx.send(
            "React with the the plus to join the game of text race - "
            "see who types the fastest"
        )
        await msg.add_reaction("\U00002795")

        def recheck(reaction, user):
            return (
                user is not ctx.author
                and reaction.message.channel == ctx.channel
                and not user.bot
                and reaction.message.id == msg.id
                and user not in players
            )

        def gamecheck(message):
            return (
                message.author in players
                and message.channel == ctx.channel
                and not message.author.bot
            )

        try:
            async with timeout(10):
                while True:
                    try:
                        reaction, user = await self.bot.wait_for(
                            "reaction_add", timeout=10.0, check=recheck
                        )
                        players.append(user)
                        await ctx.send(
                            f"User {user.mention} has joined, React with the"
                            f" \U00002795 to join the game,you still have time"
                        )
                    except (asyncio.TimeoutError):
                        continue
        except (asyncio.TimeoutError, asyncio.CancelledError):
            if len(players) < 2:
                return await ctx.send(
                    "You loose the game, since you cannot play by yourself. "
                    "**Go find some friends**"
                )

            embed = discord.Embed(
                title="Enter The sentence below first {punctuation matters, "
                      "case does not}\nYou have 20 seconds!",
                description=f"`{sent}`",
                color=ctx.guild.me.color,
            )
            embed.set_footer(
                text=f"Text game is being played by {len(players)}")
            await ctx.send(embed=embed)
            try:
                async with timeout(20):
                    while True:
                        try:
                            response = await self.bot.wait_for(
                                "message", timeout=20.0, check=gamecheck
                            )
                            if emo in response.content.lower():
                                await ctx.send(
                                    "You cheater, you have been removed from "
                                    "this game, sorry "
                                )
                                players.remove(response.author)
                            elif ans == response.content.lower():
                                return await ctx.send(
                                    f"And the winner is..........."
                                    f"{response.author.mention}"
                                )
                        except asyncio.TimeoutError:
                            continue
            except (asyncio.TimeoutError, asyncio.CancelledError):
                st = ""
                for e in players:
                    st = st + f"  {e.mention}"
                await ctx.send(
                    f"Sorry No one got it\n{st} You guys are losers")

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def numgame(self, ctx):
        y = random.randint(0, 100)
        channel = ctx.channel
        await channel.send("enter a numberer between 1 and 100")
        correct = False

        def check(guess):
            return (guess.author.id == ctx.author.id) and (
                guess.channel == channel)

        while not correct:
            try:
                guess = await self.bot.wait_for("message", timeout=30.0,
                                                check=check)
            except asyncio.TimeoutError:
                await channel.send("TIME IS UP")
                await channel.send("NUMBER WAS: {}".format(y))
            try:
                guessf = int(guess.content)
            except BaseException:
                await channel.send("ENTER NUMBERS")
            else:
                if guessf == y:
                    await channel.send("Correct")
                    correct = True
                elif guessf > y:
                    await channel.send("Number is too big")
                elif guessf < y:
                    await channel.send("Number is too small")
                else:
                    await channel.send("Unknown error")
                    break
        await channel.send("Game over!")

    @commands.command(aliases=['wyr'])
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def wouldyourather(self, ctx):
        await ctx.trigger_typing()
        rdict = await self.geteither()
        rembed = discord.Embed(
            title='Would you rather?',
            description=f"\U0001f170: {rdict['choice1']}\n**OR**\n\U0001f1e7: "
                        f"{rdict['choice2']}",
            color=ctx.guild.me.color)
        rembed.set_footer(text='You have 1 minute')
        msg = await ctx.send(embed=rembed)
        await msg.add_reaction('\U0001f170')
        await msg.add_reaction('\U0001f1e7')
        await asyncio.sleep(60)
        channel = ctx.channel
        m_id = msg.id
        mob = await channel.fetch_message(m_id)
        list_data = mob.reactions
        choice1 = int(list_data[0].count) - 1
        choice2 = int(list_data[1].count) - 1
        if choice1 > choice2:
            win = f"Choice A {rdict['choice1']} has Won!"
        else:
            win = f"Choice B {rdict['choice2']} has Won!"
        tit = choice1 + choice2
        embed = discord.Embed(
            title='Would you rather results!',
            color=ctx.guild.me.color)
        embed.description = win
        embed.add_field(name='Total Respondants', value=tit, inline=False)
        embed.add_field(
            name='Choice A',
            value=f"**Number of A**: {choice1}\n**Percent A**:"
                  f" {round(((choice1 / tit) * 100), 2)}\n**Online A Percent**"
                  f":{rdict['percentage1']} ",
            inline=True)
        embed.add_field(
            name='Choice B',
            value=f"**Number of B**: {choice2}\n**Percent B**: "
                  f"{round(((choice2 / tit) * 100), 2)}\n**Online B Percent**"
                  f":{rdict['percentage2']} ",
            inline=True)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, aliases=['ttt'])
    async def tictactoe(self, ctx):
        await ctx.send(
            'Please select use either `tictactoe comp` or `tictactoe user`')

    @tictactoe.command(aliases=['comp'])
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def computer(self, ctx):
        def gamecheck(message_check):
            return message_check.author == ctx.author \
                and message_check.channel == ctx.channel \
                and len(message_check.content) == 2

        game = TicTacToe()
        await game.makegamegrid()
        playermoves = []
        ai = 0
        user = 1
        turns = 0
        embed = discord.Embed(
            title=f'TicTacToe game. DAGBOT vs {ctx.author.display_name}',
            color=ctx.guild.me.color)
        embed.description = 'Please use letters for rows (a,b,c) and numbers \
            for columns!' + await game.gamegridprinter()
        await ctx.send(embed=embed)
        while True:
            if user == 1:
                token = 1
                try:
                    message = await self.bot.wait_for('message',
                                                      check=gamecheck,
                                                      timeout=60.0)
                except asyncio.TimeoutError:
                    return await ctx.send(
                        "No response from player exiting game")
                else:
                    text = message.content
                    try:
                        nu, nut = await game.converter(text)
                    except BaseException:
                        await ctx.send(
                            'We could not convert your input. Please use the \
                                format <letter><number> ex `a3` or `b3`')
                    else:
                        y = await game.checkempty(nu, nut)
                        if y:
                            await game.makemove(nu, nut, token)
                            ai = 1
                            user = 0
                            turns += 1
                            playermoves.append((nu, nut))
                        else:
                            await ctx.send(
                                'That game square is aldready taken please \
                                    choose another one.')

            else:
                if ai == 1:
                    nu, nut = await game.aigamemove(turns, playermoves)
                    if str(nu) == 'error':
                        break
                    else:
                        token = 2
                        await game.makemove(nu, nut, token)
                        ai = 0
                        user = 1
                        turns += 1

            grid = await game.sharegamegrid()
            resl = await game.gamecheck(grid)

            if resl[0]:
                embed = discord.Embed(
                    title=f'TicTacToe  DAGBOT vs {ctx.author.display_name}',
                    color=ctx.guild.me.color)
                embed.description = 'Please use letters for rows (a,b,c) and \
                    numbers for columns!' + await game.gamegridprinter()
                await ctx.send(embed=embed)
                if resl[1] == 0:
                    return await ctx.send(
                        f'game over. It was a tie! {ctx.author.mention}')
                elif resl[1] == 1:
                    return await ctx.send(
                        f'Guess you won. I\'ll probs win next time \
                            {ctx.author.mention}')
                else:
                    return await ctx.send(
                        f'I won get reckt. {ctx.author.mention}')
            else:
                if user == 1:
                    embed = discord.Embed(
                        title=f'TicTacToe DAGBOT vs {ctx.author.display_name}',
                        color=ctx.guild.me.color)
                    embed.description = 'Please use letters for rows (a,b,c) \
                        and numbers for columns!' + \
                        await game.gamegridprinter()
                    await ctx.send(embed=embed)

    @tictactoe.command()
    async def user(self, ctx):
        mlsit = []
        mlsit.append(ctx.author)
        msg = await ctx.send(
            f'React if you wanna join {ctx.author.mention} \
                for a game of tictactoe')
        await msg.add_reaction('<a:giftick:734746863340748892>')

        # and reaction.author != ctx.author

        def check(reaction, user):
            # print('reaction')
            return reaction.message.id == msg.id and not user.bot and str(
                reaction.emoji) == '<a:giftick:734746863340748892>'

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     check=check, timeout=60.0)

        except asyncio.TimeoutError:
            return await ctx.send(
                'sorry no one wants to play with you. \
                Maybe play with me? `ttt ai`')

        mlsit.append(user)
        game = TicTacToe()
        playermoves = []
        await game.makegamegrid()
        embed = discord.Embed(
            title=f'TicTacToe {ctx.author.display_name} vs \
                {mlsit[1].display_name}',
            color=ctx.guild.me.color)
        embed.description = 'Please use letters for rows (a,b,c) and numbers \
            for columns!' + await game.gamegridprinter()
        await ctx.send(embed=embed)

        player = 0
        turns = 0

        def p1check(message):
            return message.author == ctx.author and \
                message.channel == ctx.channel and \
                len(message.content) == 2

        def p2check(message):
            return message.author == mlsit[
                1] and message.channel == ctx.channel and len(
                message.content) == 2

        while True:
            if player == 0:
                token = 1
                try:
                    message = await self.bot.wait_for('message', check=p1check,
                                                      timeout=60.0)
                except asyncio.TimeoutError:
                    return await ctx.send(
                        f"No response from {ctx.author.mention} exiting game")
                else:
                    text = message.content
                    try:
                        nu, nut = await game.converter(text)
                    except BaseException:
                        await ctx.send(
                            'We could not convert your input. Please use the \
                                format <letter><number> ex `a3` or `b3`')
                    else:
                        y = await game.checkempty(nu, nut)
                        if y:
                            await game.makemove(nu, nut, token)
                            player = 1
                            turns += 1
                            playermoves.append((nu, nut))
                        else:
                            await ctx.send(
                                'That game square is aldready taken please \
                                    choose another one.')

            else:
                token = 2
                try:
                    message = await self.bot.wait_for('message', check=p2check,
                                                      timeout=60.0)
                except asyncio.TimeoutError:
                    return await ctx.send(
                        f"No response from {mlsit[1].mention} exiting game")
                else:
                    text = message.content
                    try:
                        nu, nut = await game.converter(text)
                    except BaseException:
                        await ctx.send(
                            'We could not convert your input. Please use the \
                                format <letter><number> ex `a3` or `b3`')
                    else:
                        y = await game.checkempty(nu, nut)
                        if y:
                            await game.makemove(nu, nut, token)
                            player = 0
                            turns += 1
                            playermoves.append((nu, nut))
                        else:
                            await ctx.send(
                                'That game square is aldready taken please \
                                    choose another one.')

            grid = await game.sharegamegrid()
            resl = await game.gamecheck(grid)

            if resl[0]:
                embed = discord.Embed(
                    title=f'TicTacToe  DAGBOT vs {ctx.author.display_name}',
                    color=ctx.guild.me.color)
                embed.description = 'Please use letters for rows (a,b,c) and \
                    numbers for columns!' + await game.gamegridprinter()
                await ctx.send(embed=embed)
                if resl[1] == 0:
                    return await ctx.send(
                        f'game over. It was a tie! {ctx.author.mention}')
                elif resl[1] == 1:
                    return await ctx.send(
                        f'{ctx.author.mention} has one this game of tictactoe. \
                            {mlsit[1].mention}')
                else:
                    return await ctx.send(
                        f'{mlsit[1].mention} has one this game of tictactoe. \
                            {ctx.author.mention}')
            else:

                embed = discord.Embed(
                    title=f'TicTacToe DAGBOT vs {ctx.author.display_name}',
                    color=ctx.guild.me.color)
                embed.description = 'Please use letters for rows (a,b,c) and \
                    numbers for columns!' + await game.gamegridprinter()
                await ctx.send(embed=embed)

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def fight(self, ctx, challenged: discord.Member):
        mlsit = []
        mlsit.append(ctx.author)
        msg = await ctx.send(
            f'{challenged.mention}.  {ctx.author.mention} has challenged you \
                to a fight! React to accept')
        await msg.add_reaction('<a:giftick:734746863340748892>')

        def check(reaction, user):
            # print('reaction')

            return reaction.message.id == msg.id and not user.bot and str(
                reaction.emoji) == '<a:giftick:734746863340748892>' and \
                user.id == challenged.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     check=check, timeout=60.0)

        except asyncio.TimeoutError:
            return await ctx.send(
                'sorry no onw wants to play with you. \
                    Maybe play with me? `ttt ai`')

        mlsit.append(challenged)
        try:
            await ctx.author.send('Game will begin shortly')
        except BaseException:
            await ctx.send(
                f'{ctx.author.mention} Your Dm\'s are closed. \
                    The game occurs in the dms')
        try:
            await mlsit[1].send('Game will negin shortly')
        except BaseException:
            await ctx.send(
                f'{mlsit[1].mention} Your Dm\'s are closed. \
                    The game occurs in the dms')

        hpa = 100
        hpb = 100
        damdict = {"kick": 25, "bite": 20, "punch": 15}
        movelist = ["kick", "block", "punch", "bite"]
        embed = discord.Embed(
            title=f"Ultimate fight {ctx.author.mention} vs {user.mention}")
        embed.description = "Please DM your move to the bot\n \
        There is a fight going on. Please choose on of the following moves \
            to use.\n**bite**: 20 damage (may miss (50% accuracy))\n**kick**: \
                25 damage (You loose 10 damage while attacking)\n**punch**: \
                    15 damage\n**block**: blocks an attack"
        embed.add_field(
            name=f"{ctx.author.display_name} HP",
            value=hpa,
            inline=True)
        embed.add_field(
            name=f"{challenged.display_name} HP",
            value=hpb,
            inline=True)
        await ctx.send(embed=embed)

        def p0check(message):
            return (
                message.author.id == ctx.author.id) and \
                message.guild is None

        def p1check(message):
            return (
                message.author.id == challenged.id) and \
                message.guild is None

        try:
            async with timeout(600):
                while True:
                    try:
                        async with timeout(60):
                            while True:
                                await ctx.author.send(
                                    'Please reply with your move to the bot.')
                                try:
                                    message = await self.bot.wait_for(
                                        'message', check=p0check, timeout=30)
                                except asyncio.TimeoutError:
                                    return await ctx.send(
                                        f'No one responded so we are \
                                        cancelling the game \
                                            {ctx.author.mention}')
                                if message.content.lower() in movelist:
                                    movea = message.content.lower()
                                    break
                    except asyncio.TimeoutError:
                        return await ctx.send(
                            f"{ctx.author.mention} \
                            You didn't make a move in time.")

                    try:
                        async with timeout(60):
                            while True:
                                await mlsit[1].send(
                                    'Please reply with your move to the bot.')
                                try:
                                    message = await self.bot.wait_for(
                                        'message', check=p1check, timeout=30)
                                except asyncio.TimeoutError:
                                    return await ctx.send(
                                        f'No one responded so we are \
                                            cancelling the game \
                                                {mlsit[1].mention}')
                                if message.content.lower() in movelist:
                                    moveb = message.content.lower()
                                    break
                    except asyncio.TimeoutError:
                        return await ctx.send(
                            "The fight got over. \
                                Please make your moves within 60s. ")
                    if movea == moveb == "block":
                        embed = discord.Embed(
                            description="Both of you vlovked each other no \
                                damage was done",
                            color=ctx.guild.me.color)
                        await ctx.send(embed=embed)
                    else:
                        if movea == "block":
                            hpa -= 5
                            actionsta = "Blocked opponent B's attack"
                        elif movea == "kick":
                            hpb -= damdict["kick"]
                            hpa -= 10
                            actionsta = "Used kick and caused 25 damage \
                                but lost 5 health"
                        elif movea == "bite":
                            r = random.randint(1, 2)
                            if r == 2:
                                actionsta = "Used bite but missed"
                            else:
                                hpb -= damdict["bite"]
                                actionsta = "Used bite and caused 20 damage"
                        else:
                            hpb -= damdict["punch"]
                            actionsta = "Used punch and caused 15 damage"
                        if moveb == "block":
                            hpb -= 5
                            actionstb = "Blocked opponent B's attack"
                        elif moveb == "kick":
                            hpa -= damdict["kick"]
                            hpb -= 10
                            actionstb = "Used kick and caused 25 damage but \
                                lost 5 health"
                        elif moveb == "bite":
                            r = random.randint(1, 2)
                            if r == 2:
                                actionstb = "Used bite but missed"
                            else:
                                hpa -= damdict["bite"]
                                actionstb = "Used bite and caused 20 damage"
                        else:
                            hpa -= damdict["punch"]
                            actionstb = "Used punch and caused 15 damage"
                        if hpa < 0 and hpb < 0 and hpa == hpb:
                            return await ctx.send(
                                f'{ctx.author.mention} and {mlsit[1].mention} \
                                have gaught and tha match is a draw')
                        elif abs(hpb) < abs(hpa) and hpa <= 0 and hpb <= 0:
                            return await ctx.send(
                                f'{ctx.author.mention} has beaten  \
                                    {mlsit[1].mention} in a fight')
                        elif abs(hpa) > abs(hpb) and hpa <= 0 and hpb <= 0:
                            return await ctx.send(
                                f'{mlsit[1].mention} has beaten  \
                                    {ctx.author.mention} in a fight')
                        else:
                            embed = discord.Embed(
                                title="Round results. The fight is \
                                    still on going",
                                color=ctx.guild.me.color)
                            embed.description = f'{ctx.author.mention} VS \
                                {mlsit[1].mention}'
                            embed.add_field(
                                name=f"{ctx.author.display_name} HP",
                                value=hpa, inline=True)
                            embed.add_field(
                                name=f"{challenged.display_name} HP",
                                value=hpb, inline=True)
                            embed.add_field(
                                name=f"Player A {ctx.author.display_name}",
                                value=actionsta,
                                inline=False)
                            embed.add_field(
                                name=f"Player B {mlsit[1].display_name}",
                                value=actionstb,
                                inline=False)
                            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send(
                'Bruh if you don\'t finish the fight within the first \
                    10 minutes the cops might show up')

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def wtp(self, ctx):
        obj = await self.bot.dagpi.wtp()
        rjs = obj.dict
        q = rjs['question_image']
        a = rjs['answer_image']
        name = rjs['pokemon']['name']
        embed = discord.Embed(
            title='Whose That Pokemon?',
            color=ctx.guild.me.color)
        embed.set_image(url=q)
        await ctx.send(embed=embed)

        def func(message):
            return message.channel == ctx.channel and not message.author.bot

        try:
            async with timeout(120):
                while True:
                    try:
                        message = await self.bot.wait_for('message',
                                                          check=func,
                                                          timeout=20.0)
                    except BaseException:
                        embed = discord.Embed(
                            title='No answesrs for some time',
                            description=f'The pokemon was **{name}**',
                            color=ctx.guild.me.color)
                        embed.set_image(url=a)
                        return await ctx.send(embed=embed)
                    if message.content.lower() == name.lower():
                        embed = discord.Embed(
                            title=f'{message.author.display_name} \
                                got the Pokemon!',
                            description=f'The pokemon was **{name}**',
                            color=ctx.guild.me.color)
                        embed.set_image(url=a)
                        return await ctx.send(embed=embed)
                    elif (message.content.lower() == 'cancel') and \
                         (message.author == ctx.author):
                        embed = discord.Embed(
                            title='Game Cancelled',
                            description=f'The pokemon was **{name}**',
                            color=ctx.guild.me.color)
                        embed.set_image(url=a)
                        return await ctx.send(embed=embed)
                    else:
                        continue
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title='No one got the pokemon',
                description=f'The pokemon was **{name}**',
                color=ctx.guild.me.color)
            embed.set_image(url=a)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def logogame(self, ctx):
        obj = await self.bot.dagpi.logo()
        rjs = obj.dict
        q = rjs['question']
        a = rjs['answer']
        name = rjs['brand']
        url = rjs['wiki_url'].replace(' ', '_')
        hint = rjs['hint']
        easy = rjs['easy']
        embed = discord.Embed(
            title='Guess the brand',
            color=ctx.guild.me.color)
        embed.add_field(name='Difficulty', value='easy' if easy else 'hard')
        embed.set_footer(text='Use a `hint` for a hint to help!')
        embed.set_image(url=q)
        await ctx.send(embed=embed)

        def func(message):
            return message.channel == ctx.channel and not message.author.bot

        try:
            async with timeout(120):
                while True:
                    try:
                        message = await self.bot.wait_for('message',
                                                          check=func,
                                                          timeout=20.0)
                    except BaseException:
                        embed = discord.Embed(
                            title='No answers for some time',
                            description=f'The logo was **{name}**',
                            color=ctx.guild.me.color,
                            url=url)
                        if rjs['easy']:
                            embed.add_field(
                                name='Description', value=rjs['clue'])
                        embed.set_image(url=a)
                        return await ctx.send(embed=embed)
                    if message.content.lower() == name.lower():
                        embed = discord.Embed(
                            title=f'{message.author.display_name} \
                                got the brand!',
                            description=f'The Brand was **{name}**',
                            color=ctx.guild.me.color,
                            url=url)
                        embed.set_image(url=a)
                        if rjs['easy']:
                            embed.add_field(
                                name='Description', value=rjs['clue'])
                        return await ctx.send(embed=embed)
                    elif (message.content.lower() == 'hint') and \
                         (message.author == ctx.author):
                        embed = discord.Embed(
                            title='Logo Game Hint',
                            description=f'`{hint}`',
                            color=ctx.guild.me.color)
                        await ctx.send(embed=embed)
                    elif (message.content.lower() == 'cancel') and \
                         (message.author == ctx.author):
                        embed = discord.Embed(
                            title='Game Cancelled',
                            description=f'The logo was **{name}**',
                            color=ctx.guild.me.color,
                            url=url)
                        if rjs['easy']:
                            embed.add_field(
                                name='Description', value=rjs['clue'])
                        embed.set_image(url=a)
                        return await ctx.send(embed=embed)
                    else:
                        continue
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title='No one got the Brand',
                description=f'The Brand was **{name}**',
                color=ctx.guild.me.color,
                url=url)
            if rjs['easy']:
                embed.add_field(name='Description', value=rjs['clue'])
            embed.set_image(url=a)
            await ctx.send(embed=embed)
