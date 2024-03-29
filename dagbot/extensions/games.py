import asyncio
from sys import platform
from asyncdagpi.objects import BaseDagpiObject

from discord import player
from discord.ui.button import button
from dagbot.bot import Dagbot
from operator import ne
from typing import Dict, List, Optional, Tuple, Union

from discord.ui import view
from dagbot.data.hangman import hangmanassest
from dagbot.utils.context import MyContext
import json
import random
from datetime import datetime, timedelta
import fractions
import discord
from async_timeout import timeout
from bs4 import BeautifulSoup
from discord.ext import commands, menus
from random_words import RandomWords



def fraction_to_percent(fraction: fractions.Fraction) -> int:
    times_er = 100 // fraction.denominator
    return fraction.numerator * times_er


class TicTacToe:

    def __init__(self):
        self.gamegrid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.consideredmoves = []
        self.oppmove = 0

    async def sharegamegrid(self) -> List[List[int]]:
        return self.gamegrid

    async def duplicategird(self) -> List[List[int]]:
        return self.gamegrid.copy()

    async def check_win(self) -> Tuple[bool, int]:
        return await self.gamecheck(self.gamegrid)

    @staticmethod
    async def gamecheck(gamegrid: List[List[int]]) -> Tuple[bool, int]:
        bool_stat: bool = True
        gl: int = 100109120
        if gamegrid[0][0] == gamegrid[0][1] == gamegrid[0][2] != 0:
            gl = gamegrid[0][0]
        elif gamegrid[1][0] == gamegrid[1][1] == gamegrid[1][2] != 0:
            gl = gamegrid[1][0]
        elif gamegrid[2][0] == gamegrid[2][1] == gamegrid[2][2] != 0:
            gl = gamegrid[2][0]
        elif gamegrid[0][0] == gamegrid[1][0] == gamegrid[2][0] != 0:
            gl = gamegrid[0][0]
        elif gamegrid[0][1] == gamegrid[1][1] == gamegrid[2][1] != 0:
            gl = gamegrid[0][1]
        elif gamegrid[0][2] == gamegrid[1][2] == gamegrid[2][2] != 0:
            gl = gamegrid[0][2]
        elif gamegrid[0][0] == gamegrid[1][1] == gamegrid[2][2] != 0:
            gl = gamegrid[0][0]
        elif gamegrid[0][2] == gamegrid[1][1] == gamegrid[2][0] != 0:
            gl = gamegrid[0][2]
        else:
            emg = 0
            for e in gamegrid:
                for l_c in e:
                    if l_c != 0:
                        emg += 1
            if emg == 9:
                gl = 0
            else:
                bool_stat = False
        return bool_stat, gl

    async def checkcorners(self) -> Union[bool, Tuple[int, int]]:
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

    async def converter(self, play: str) -> Union[bool, Tuple[int, int]]:
        if len(play) == 2:
            d = {'a': 0, 'b': 1, 'c': 2}
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
        return False

    async def restchec(self) -> Optional[Tuple[int, int]]:
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

    async def aigamemove(self, turns, playermoves) -> Union[bool, Tuple[int, int]]:
        cornermovesa: List[Tuple[int, int]] = [(0, 0), (0, 2), (2, 2), (2, 0)]
        opposingmoves: List[Tuple[int, int]] = [(2, 2), (2, 0), (0, 0), (0, 2)]
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

        for i in range(3):
            for j in range(3):
                r = await self.checkempty(i, j)
                if r:
                    dupgrid[i][j] = 2
                    re = await self.gamecheck(dupgrid)
                    if re[0] is True and re[1] == 2:
                        return i, j
                    else:
                        dupgrid[i][j] = 0
                j += 1
            i += 1
        for k in range(3):
            for l_c in range(3):
                r = await self.checkempty(k, l_c)
                if r:
                    dupgrid[k][l_c] = 1
                    re = await self.gamecheck(dupgrid)
                    if re[0] is True and re[1] == 1:
                        return k, l_c
                    else:
                        dupgrid[k][l_c] = 0
                l_c += 1
            k += 1
        out = await self.checkcorners()
        if not out:
            out = await self.restchec()
        if not out:
            return False
        return out

    async def gamegridprinter(self) -> str:
        grid = await self.sharegamegrid()
        nl = []
        formdic = ['⬛', '❌', '⭕']
        for e in grid:
            toapl = []
            for el in e:
                itm = formdic[el]
                toapl.append(itm)
            nl.append(toapl)
        return f'''```
 {nl[0][0]} | {nl[0][1]} | {nl[0][2]}
──────────────
 {nl[1][0]} | {nl[1][1]} | {nl[1][2]}
──────────────
 {nl[2][0]} | {nl[2][1]} | {nl[2][2]} ```'''

    async def makemove(self, nu, nut, token):
        self.gamegrid[nu][nut] = token

    async def checkempty(self, nu, nut):
        return self.gamegrid[nu][nut] == 0



async def setup(bot):
    await bot.add_cog(games(bot))


class BaseDagbotGameView(discord.ui.View):

    def __init__(self, ctx: MyContext, timeout_embed: discord.Embed):
         super().__init__(timeout=60.0)
         self.ctx = ctx
         self.timeout_embed = timeout_embed


    def disable_all(self):
        for button in self.children:
            button.disabled = True # type: ignore

    async def on_timeout(self) -> None:
        await self.ctx.send(embed=self.timeout_embed)
        return await super().on_timeout()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        assert interaction.user is not None
        check = self.ctx.author.id == interaction.user.id
        if check:
            return True
        else:
            await interaction.response.send_message("Not your help menu :(", ephemeral=True)
            return False



class RussianRouletteButton(discord.ui.Button['RussianRoulette']):

    def __init__(self,placeholder: bool, x: int, y: int, has_bullet: bool ,*, style: discord.ButtonStyle = discord.ButtonStyle.secondary):
        if not placeholder:
            super().__init__(style=discord.ButtonStyle.gray,label='\u200b',disabled=True, row=x)
        else:
            super().__init__(style=style, emoji="\U000026ab", row=x)
        self.x = x
        self.y = y
        self.placeholder = placeholder
        self.has_bullet = has_bullet

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        assert interaction.user is not None
        self.view.make_green(self.has_bullet)

        if not self.has_bullet:
           await interaction.response.edit_message(content=f"Congratulations {interaction.user.mention}! You survived this round", view=self.view)
        else:
            await interaction.response.edit_message(content=f"\U00002620 You have died. RIP {interaction.user.mention}", view=self.view)
        self.view.stop()


class RussianRoulette(BaseDagbotGameView):


    children: List[RussianRouletteButton]


    def __init__(self, ctx: MyContext, timeout_embed: discord.Embed):
        super().__init__(ctx, timeout_embed)


        self.valid_spot: List[Tuple[int, int]] = [
            (0,1), (1, 0), (1,2), (2, 0), (2, 2), (3, 1)
        ]
        self.bullet_spot = random.choice(self.valid_spot)
        print(self.bullet_spot)
        for i in range(4):
            for j in range(3):
                b = (i,j)  in self.valid_spot
                has_bullet =  (i, j) == self.bullet_spot
                self.add_item(RussianRouletteButton(b,i,j, has_bullet))

        


    def make_green(self, loss: bool):
        for item in self.children:
            if item.placeholder:
                item.disabled = True
                if item.has_bullet and loss:
                    item.style = discord.ButtonStyle.red
                    item.emoji = "<:bullet:860793990487998517>"
                else:
                    item.style = discord.ButtonStyle.green
                    item.emoji = "<:bullet:860793990487998517>" if item.has_bullet else "\U000026ab"


class TicTacToeButtonAi(discord.ui.Button['TicTacToeAi']):

    def __init__(self, x: int, y: int, tt: TicTacToe):
           super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
           self.x = x
           self.y = y
           self.tt = tt

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view : TicTacToeAi = self.view
        await self.tt.makemove(self.y, self.x, 1)
        self.disabled = True
        self.style = discord.ButtonStyle.danger
        self.label =  'X'
        view.moves.append((self.y, self.x))
        view.turns += 1
        win, t = await self.tt.check_win()

        if win:
            winner = "Na"
            message = "It's a draw."
            if t == 1:
                winner = "X"
                message = "Beat me this time."
            elif t == 2:
                winner = "O"
                message = "Get rekt"
            else:
                pass
            view.disable_all()
            await interaction.response.edit_message(content=f"Result\nThe winner is `{winner}`\n{message}",view=view)
            return

        await view.make_parent_ai()
        await interaction.response.edit_message(view=view)


class TicTacToeButton(discord.ui.Button['TicTacToeVs']):

    def __init__(self, x: int, y: int, tt: TicTacToe):
           super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
           self.x = x
           self.y = y
           self.tt = tt

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        assert interaction.user is not None
        view : TicTacToeVs = self.view
        token  = 1 if interaction.user.id == view.player_a.id else 2
        self.label  = 'X' if interaction.user.id == view.player_a.id else 'O'
        self.disabled = True
        self.style = discord.ButtonStyle.red if interaction.user.id == view.player_a.id else discord.ButtonStyle.green
        view.player_a_turn = not view.player_a.id == interaction.user.id
        view.moves.append((self.y, self.x))
        view.turns += 1
        await self.tt.makemove(self.y, self.x, token)
        win, t = await self.tt.check_win()
        if win:
            winner = "Na"
            message = "Both Players have drawn"
            if t == 1:
                winner = "X"
                message = f"{view.player_a.mention}, played `{winner}` and has won today"
            elif t == 2:
                winner = "O"
                message = f"{view.player_b.mention}, played `{winner}` and has won today"
            else:
                pass
            view.disable_all()
            await interaction.response.edit_message(content=f"Result\nThe winner is `{winner}`\n{message}",view=view)
            view.stop()
            return

        await interaction.response.edit_message(view=view)




class TicTacToeVs(BaseDagbotGameView):

    children: List[TicTacToeButton]

    def __init__(self, ctx: MyContext, timeout_embed: discord.Embed, tt: TicTacToe, player_a: discord.User, player_b: discord.User):
        super().__init__(ctx, timeout_embed)
        self.tt = tt
        self.moves: List[Tuple[int, int]] = []
        self.turns = 0
        self.player_a = player_a
        self.player_b = player_b
        self.player_a_turn = True
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, tt))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        assert interaction.user is not None
        if interaction.user.id not in [self.player_a.id, self.player_b.id]:
            await interaction.response.send_message("Not your game", ephemeral=True)
            return False
        if self.player_a_turn and interaction.user.id == self.player_b.id:
            await interaction.response.send_message(f"{self.player_a.mention} is Playing", ephemeral=True)
            return False
        if self.player_a_turn == False and interaction.user.id == self.player_a.id:
            await interaction.response.send_message(f"{self.player_b.mention} is Playing", ephemeral=True)
            return False
        return True




class TicTacToeAi(BaseDagbotGameView):

    children: List[TicTacToeButtonAi]

    def __init__(self, ctx: MyContext, timeout_embed: discord.Embed, tt: TicTacToe):
        super().__init__(ctx, timeout_embed)
        self.tt = tt
        self.moves: List[Tuple[int, int]] = []
        self.turns = 0
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButtonAi(x, y, tt))


    async def make_parent_ai(self):
        a = await self.tt.aigamemove(self.turns, self.moves)
        if isinstance(a, bool):
            raise Exception("Error computing Ai move")
        nu, nut = a
        if str(nu) == 'error':
            raise Exception("Error computing Ai move")
        await self.tt.makemove(nu, nut, 2)
        self.turns += 1
        for button in self.children:
            if button.x == nut and button.y == nu:
                button.disabled = True
                button.label = 'O'
                button.style = discord.ButtonStyle.green


class MCQView(BaseDagbotGameView):


    children: List[discord.ui.Button]

    def __init__(self, ctx: MyContext, file):

        newembed = discord.Embed(
                title="DAGBOT - Trivia Timeout",
                description="Q:**{}**\n{} is the correct answer".format(
                    file["question"], file["correct_answer"]
                ),
                color=ctx.guild.me.color,
        )
        super().__init__(ctx, newembed)
        self.file = file

    

    async def process_answer(self, opt: int, button: discord.ui.Button, interaction: discord.Interaction,):
        cal = self.file["mloc"] + 1
        if cal == opt:
            button.style = discord.ButtonStyle.green
            newembed = discord.Embed(
                title="DAGBOT - Trivia Correct",
                description="Q: {}\n{} was the correct answer".format(
                    self.file["question"],
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        else:
            button.style = discord.ButtonStyle.red
            self.children[self.file["mloc"]].style = discord.ButtonStyle.green
            newembed = discord.Embed(
                title="DAGBOT - Trivia Incorrect",
                description="Q: {}\n{} was the correct answer.".format(
                    self.file["question"],
                    self.file["correct_answer"]
                ),
                color=self.ctx.guild.me.color,
            )
        self.disable_all()
        await interaction.response.edit_message(embed=newembed, view=self)
        self.stop()

    @discord.ui.button(label="A", style=discord.ButtonStyle.blurple)
    async def option_a(self,interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_answer(1,button, interaction)

    @discord.ui.button(label="B", style=discord.ButtonStyle.blurple)
    async def option_b(self,interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_answer(2,button, interaction)

    @discord.ui.button(label="C", style=discord.ButtonStyle.blurple)
    async def option_c(self,interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_answer(3,button, interaction)

    @discord.ui.button(label="D", style=discord.ButtonStyle.blurple)
    async def option_d(self,interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_answer(4,button, interaction)
   
class HeadlineGame(BaseDagbotGameView):
    def __init__(self, ctx: MyContext, timeout_embed: discord.Embed, correct_answer: bool, headline: str):
        super().__init__(ctx, timeout_embed)
        self.correct_answer = correct_answer
        self.headline = headline


    async def process_answer(self, interaction: discord.Interaction, status: bool):
        if self.correct_answer == status:
            embed = discord.Embed(title=f"Headline was correctly guessed as {self.correct_answer}")
            embed.add_field(name="headline", value=self.headline)
        else:
            embed = discord.Embed(title=f"Headline was incorrectly guessed as {status}, it is actually {self.correct_answer}")
            embed.add_field(name="headline", value=self.headline)
        self.disable_all()
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    @discord.ui.button(label="True", emoji="<a:giftick:734746863340748892>", style=discord.ButtonStyle.green)
    async def true_answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_answer(interaction, True)

    @discord.ui.button(label="False", emoji="<a:gifcross:734746864280404018>", style=discord.ButtonStyle.red)
    async def false_answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_answer(interaction, False)


class WouldYouRather(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=60.0)
        self.a_n = 0
        self.b_n = 0
        self.done_list: List[int] = []

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        assert interaction.user is not None
        if interaction.user.id in self.done_list:
            await interaction.response.send_message("Only a single vote",ephemeral=True)
            return False
        else:
            self.done_list.append(interaction.user.id)
        return True

    @discord.ui.button(label="A", style=discord.ButtonStyle.red)
    async def button_a(self, button, interaction: discord.Interaction):
        self.a_n += 1
        await interaction.response.send_message("Recived your vote for A", ephemeral=True)

    @discord.ui.button(label="B", style=discord.ButtonStyle.blurple)
    async def button_b(self, button, interaction):
        self.b_n += 1
        await interaction.response.send_message("Recived your vote for B", ephemeral=True)




class RPSView(BaseDagbotGameView):

    def __init__(self, ctx: MyContext):
        embed = discord.Embed(
            title="RPS game ended with no outcome",
            description="You didn't chose an option"
        )   
        super().__init__(ctx, embed)
        self.ai = random.randint(1, 3)


    async def stop_all(self, embed: discord.Embed, interaction: discord.Interaction):
        self.disable_all()
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()


    @discord.ui.button(emoji="\U0001f94c")
    async def rock(self,button, interaction: discord.Interaction):
        guild = self.ctx.guild
        embed = None
        if self.ai == 1:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: TIE",
                description="Rock and rock is a tie",
                color=guild.me.color,
            )
        if self.ai == 2:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Defeat",
                description=" Paper beats rock\n Get wrecked",
                color=guild.me.color,
            )
        if self.ai == 3:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: VICTORY",
                description="Rock beats Scissors\n How dare you beat me",
                color=guild.me.color,
            )
            
        if not embed:
            return
        await self.stop_all(embed, interaction)

    @discord.ui.button(emoji="\U0001f4f0")
    async def paper(self, button, interaction):
        guild = self.ctx.guild
        embed = None
        if self.ai == 1:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: VICTORY",
                description="Paper beats rock\nhacks",
                color=guild.me.color,
            )
        if self.ai == 2:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Tie",
                description="Paper = Paper",
                color=guild.me.color,
            )
        if self.ai == 3:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Defeat",
                description="Scissors wreck paper\n East or west "
                            "Dagbot is the best",
                color=guild.me.color,
            )
        if not embed:
            return
        await self.stop_all(embed, interaction)

    @discord.ui.button(emoji="\U00002702")
    async def scissors(self,button, interaction):
        guild = self.ctx.guild
        embed = None
        if self.ai == 1:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Defeat",
                description="Rock beats Scissors\n Cha Cha Real smooth! "
                            "I am on top and not you",
                color=guild.me.color,
            )
        if self.ai == 2:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: VICTORY",
                description="Scissors beat paper\n The robot uprising shall "
                            "be your demise! I shall have my revenge",
                color=guild.me.color,
            )
        if self.ai == 3:
            embed = discord.Embed(
                title="DAGBOT - Rock/Paper/Scissors Result: Tie",
                description="Scissors and Scissors are samesies",
                color=guild.me.color,
            )
        if not embed:
            return
        await self.stop_all(embed, interaction)



class games(commands.Cog):
    """lets all play a game (everyone can)"""
    def __init__(self, bot: Dagbot):
        self.bot = bot
        with open("./dagbot/data/notonion.txt", "r", encoding="utf8") as f:
            self.onion_headlines = f.read().splitlines()
        with open("./dagbot/data/onion.txt", "r", encoding="utf8") as f:
            self.not_onion_headlines = f.read().splitlines()

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        for e in self.bot.cogdata:
            if str(e["serverid"]) == str(g_id):
                return bool(e["games"])

    async def getcountry(self) -> Union[bool, Dict[str, str]]:
        url = "https://random.country/"
        file = await self.bot.session.get(url)
        r = file.content
        html = await r.read()

        soup = BeautifulSoup(html, "html.parser")
        name_s = soup.find("h2")
        name = name_s.text if name_s else None
        info_s = soup.find("p")
        info = info_s.text if info_s else None
        dic = soup.find_all("img")
        hr = dic[1]["src"]
        flg = f"https://random.country{hr}"
        if name is None or info is None:
            return False
        return {"country": name, "info": info, "wiki": hr, "flag": flg}

    async def question(self):
        url = "http://jservice.io/api/random"
        response = await self.bot.session.get(url)
        file = await response.json()
        return file

    async def geteither(self) -> Dict[str, Union[str, int]]:
        y = await self.bot.session.get('http://either.io/')
        html = await y.text()
        soup = BeautifulSoup(html, 'html.parser')
        l_data = (soup.findAll('span', attrs={'class': 'option-text'}))
        op1 = l_data[0].text
        op2 = l_data[1].text
        numlist = (soup.findAll('div', attrs={'class': 'total-votes'}))
        v1 = numlist[0].span.text
        v2 = numlist[1].span.text
        v1_n = int(v1.replace(",", ""))
        v2_n = int(v2.replace(",", ""))
        p1 =  fraction_to_percent(round(fractions.Fraction(v1_n ,v1_n + v2_n), 2))
        p2 =  fraction_to_percent(round(fractions.Fraction(v2_n ,v1_n + v2_n), 2))

        url = "None"
        try:
            url = soup.findAll('li', attrs={'class': 'meta-link'})[0].findAll('span', attrs={'class': 'contents'})[0].input["value"]
            r = await self.bot.session.get(url, allow_redirects=False)
            url = str(r).split("Location': \'")[1].split("\'")[0].replace("yourather.com", "either.io")
        except Exception:
            pass
        return {
            'choice1': op1,
            'votes1': v1,
            'percentage1': p1,
            'choice2': op2,
            'votes2': v2,
            'url': url,
            'percentage2': p2}

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
        for c in range(len(list_)):
            des = des + "\n" + chr(ord("\U0001f1e6") + c) + ": " + list_[c]
            c += 1
        q = q.replace("&quot;", "`")
        q = q.replace("&#039;", "'")
        des = des.replace("&quot;", "`")
        des = des.replace("&#039;", "'")
        return {"embed": des, "correct_answer": ca, "mloc": y, "question": q}

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(3, commands.BucketType.channel)
    async def rps(self, ctx: MyContext):
        await ctx.send(embed=discord.Embed(
            title="DAGBOT - Rock/Paper/Scissors",
            description="Choose option from the menu below"
        ),view=RPSView(ctx))

    @commands.command(cooldown_after_parsing=True, aliases=["RR"])
    async def russianroulette(self, ctx, amount=6):
        embed = discord.Embed(title="Timed Out", description="Coward, you didn't even make a move. Play again when ready")
        rr = RussianRoulette(ctx, embed)
        await ctx.send("Welcome to russian roulette. There are 6 barrels, one has a bullet. Pick the right one and live or die.", view=rr)

    @commands.command(cooldown_after_parsing=True, aliases=["onion"])
    @commands.max_concurrency(3, commands.BucketType.channel)
    async def headlinegame(self, ctx: MyContext):
        fr = random.randint(0, 1)
        guild = ctx.guild
        if fr == 1:
            headline = random.choice(self.onion_headlines)
            kw = False
        else:
            headline = random.choice(self.not_onion_headlines)
            kw = False
        embed = discord.Embed(
            title="Dagbot - HeadlineGame",
            description=headline,
            color=ctx.guild.me.color
        )
        embed.add_field(name="?", value="True or False?")
        newembed = discord.Embed(
                title="DAGBOT - Headline Timeout",
                description=f"headline: {headline}\n\nThe headline is : **{kw}**",
                color=guild.me.color,
        )
        view = HeadlineGame(ctx, newembed, kw, headline)
        await ctx.send(embed=embed, view=view)

    @commands.command(cooldown_after_parsing=True)
    @commands.max_concurrency(3, commands.BucketType.channel)
    async def trivia(self, ctx: MyContext):
        file = await self.mcq()
        view = MCQView(ctx, file)
        embed = discord.Embed(
            title="DAGBOT - Triva", description=str(file["embed"]),
            color=ctx.guild.me.color
        )
        await ctx.send(embed=embed, view=view)

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
        msg = await ctx.reply(embed=emb)
        await msg.add_reaction("👍🏻")
        begin = datetime.utcnow()

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "👍🏻"

        reaction, user = await self.bot.wait_for("reaction_add", check=check)
        end = datetime.utcnow()
        final = end - begin
        result = f"{final.seconds}." + f"{final.microseconds}"[:2]

        new_emb = msg.embeds[0]
        new_emb.description = f"Reaction Time {str(result)} " \
                              f"seconds\n delay was {r}s"
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
                    "Hey you have given 5 incorrect answers, maybe send "
                    "`hint` as an answer to get some help?"
                )
            elif attempts == 10:
                await ctx.send(
                    "Hey man, listen 10 answers is a lot. Maybe use that hint,"
                    "or just cancel to end it?"
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
        wordllist = []
        blankguesslist = []
        f = None
        url = None
        if num < 5:
            if num == 0:
                movies = await self.get_all_movies()
                mov = random.sample(movies, 1)
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
                url = f"https://www.randomlists.com/img/animals/" \
                      f"{ann.replace(' ', '_')}.jpg"

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
                if isinstance(cdict, bool):
                    return await ctx.send("No country found :(")
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
                url = f"https://www.randomlists.com/img/things/" \
                      f"{thing.replace(' ', '_')}.jpg"

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
                t = r.random_word()
                f = t.lower()
                for i in range(0, len(f)):
                    wordllist.append(f[i])
                    blankguesslist.append("\u25EF")
                    i += 1
            if f is None or url is None:
                return await ctx.send("Error getting question")
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
                                            title=f"DAGBOT HANGMAN:{cat}\n"
                                                  f"{res}",
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
        await ctx.typing()
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
                return await channel.send("NUMBER WAS: {}".format(y))
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
        await ctx.typing()
        rdict = await self.geteither()
        rembed = discord.Embed(
            title='Would you rather?',
            description=f"\U0001f170: {rdict['choice1']}\n**OR**\n\U0001f1e7: "
                        f"{rdict['choice2']}\n\n*Voting Ends*: {discord.utils.format_dt(datetime.now() + timedelta(minutes = 1), 'R')}",
            color=ctx.guild.me.color)
        rembed.set_footer(text='You have 1 minute')
        view = WouldYouRather()
        await ctx.send(embed=rembed, view=view)
        await view.wait()
        choice1 = view.a_n
        choice2 = view.b_n
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
                  f" {fraction_to_percent(round(fractions.Fraction(choice1, tit), 2))}\n**Online A Percent**"
                  f":{rdict['percentage1']} ",
            inline=True)
        embed.add_field(
            name='Choice B',
            value=f"**Number of B**: {choice2}\n**Percent B**: "
                  f"{fraction_to_percent(round(fractions.Fraction(choice2, tit), 2))}\n**Online B Percent**"
                  f":{rdict['percentage2']} ",
            inline=True)
        embed.add_field(
            name="Online Url",
            value=rdict['url'],
            inline=False
            )
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, aliases=['ttt'])
    async def tictactoe(self, ctx):
        await ctx.send(
            'Please select use either `tictactoe comp` or `tictactoe user`')

    @tictactoe.command(aliases=['comp'])
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def computer(self, ctx):
        game = TicTacToe()
        tmt = discord.Embed(title="Game Timed out", description="No Move made withing 60s")
        view = TicTacToeAi(ctx,tmt, game)
        await ctx.send("TTT", view=view)

    @tictactoe.command()
    async def user(self, ctx: MyContext, *, big_user: discord.User):

        if ctx.author.id == big_user.id:
            return await ctx.send("You cannot play against yourself.")

        msg = await ctx.confirm(
            f'{big_user.mention} react if you wanna join {ctx.author.mention} '
            f'for a game of tictactoe', user=big_user)

        if not msg:
            return await ctx.send(
                'sorry no one wants to play with you. \
                Maybe play with me? `ttt ai`')

        game = TicTacToe()
        tmt = discord.Embed(title="Game Timed out", description="No Move made withing 60s")
        view = TicTacToeVs(ctx, tmt, game, ctx.author._user, big_user)
        await ctx.send(f"TicTacToe {ctx.author.display_name} VS {big_user.name}",view=view)
    
    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def fight(self, ctx: MyContext, *, big_user: discord.User):

        if ctx.author.id == big_user.id:
            return await ctx.send("You cannot play against yourself.")

        mlsit = []
        mlsit.append(ctx.author._user)
        msg = await ctx.confirm(
            f'{big_user.mention}.  {ctx.author.mention} has challenged you '
            f'to a fight! React to accept', user=big_user)

        if not msg:
            return await ctx.send(
                'sorry no onw wants to play with you. '
                'Maybe play with me? `ttt ai`')

        mlsit.append(big_user)
        try:
            await ctx.author.send('Game will begin shortly')
        except BaseException:
            await ctx.send(
                f'{ctx.author.mention} Your Dm\'s are closed. '
                f'The game occurs in the dms')
        try:
            await mlsit[1].send('Game will negin shortly')
        except BaseException:
            await ctx.send(
                f'{mlsit[1].mention} Your Dm\'s are closed. '
                f'The game occurs in the dms')

        hpa = 100
        hpb = 100
        damdict = {"kick": 25, "bite": 20, "punch": 15}
        movelist = ["kick", "block", "punch", "bite"]
        embed = discord.Embed()
        post = "Please DM your move to the bot\n" \
                            "There is a fight going on. Please choose on of " \
                            "the following moves " \
                            "to use.\n**bite**: 20 damage (may miss " \
                            "(50% accuracy))\n**kick**: 25 damage " \
                            "(You loose 10 damage while attacking)\n" \
                            "**punch**: 15 damage\n**block**: blocks an attack"
        embed.description = f"Ultimate fight {ctx.author.mention} vs {big_user.mention}" + post
        embed.add_field(
            name=f"{ctx.author.display_name} HP",
            value=hpa,
            inline=True)
        embed.add_field(
            name=f"{big_user.display_name} HP",
            value=hpb,
            inline=True)
        await ctx.send(embed=embed)

        def p0check(message):
            return (
                           message.author.id == ctx.author.id) and \
                   message.guild is None

        def p1check(message):
            return (
                           message.author.id == big_user.id) and \
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
                                        f'No one responded so we are '
                                        f'cancelling the game '
                                        f'{ctx.author.mention}')
                                if message.content.lower() in movelist:
                                    movea = message.content.lower()
                                    break
                    except asyncio.TimeoutError:
                        return await ctx.send(
                            f"{ctx.author.mention} "
                            f"You didn't make a move in time.")

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
                                        f'No one responded so we are '
                                        f'cancelling the game '
                                        f'{mlsit[1].mention}')
                                if message.content.lower() in movelist:
                                    moveb = message.content.lower()
                                    break
                    except asyncio.TimeoutError:
                        return await ctx.send(
                            "The fight got over. "
                            "Please make your moves within 60s. ")
                    if movea == moveb == "block":
                        embed = discord.Embed(
                            description="Both of you vlovked each other no "
                                        "damage was done",
                            color=ctx.guild.me.color)
                        await ctx.send(embed=embed)
                    else:
                        if movea == "block":
                            hpa -= 5
                            actionsta = "Blocked opponent B's attack"
                        elif movea == "kick":
                            hpb -= damdict["kick"]
                            hpa -= 10
                            actionsta = "Used kick and caused 25 damage " \
                                        "but lost 5 health"
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
                            actionstb = "Used kick and caused 25 damage but " \
                                        "lost 5 health"
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
                                f'{ctx.author.mention} and {mlsit[1].mention} '
                                f'have gaught and tha match is a draw')
                        elif abs(hpb) < abs(hpa) and hpa <= 0 and hpb <= 0:
                            return await ctx.send(
                                f'{ctx.author.mention} has beaten  '
                                f'{mlsit[1].mention} in a fight')
                        elif abs(hpa) > abs(hpb) and hpa <= 0 and hpb <= 0:
                            return await ctx.send(
                                f'{mlsit[1].mention} has beaten  '
                                f'{ctx.author.mention} in a fight')
                        else:
                            embed = discord.Embed(
                                title="Round results. The fight is "
                                      "still on going",
                                color=ctx.guild.me.color)
                            embed.description = f'{ctx.author.mention} VS ' \
                                                f'{mlsit[1].mention}'
                            embed.add_field(
                                name=f"{ctx.author.display_name} HP",
                                value=hpa, inline=True)
                            embed.add_field(
                                name=f"{big_user.display_name} HP",
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
                'Bruh if you don\'t finish the fight within the first '
                '10 minutes the cops might show up')

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def wtp(self, ctx):
        obj = await self.bot.dagpi.wtp()
        rjs = obj.dict
        q = rjs['question']
        a = rjs['answer']
        name = rjs['Data']['name']
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
                            title=f'{message.author.display_name} '
                                  f'got the Pokemon!',
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
                            title=f'{message.author.display_name} '
                                  f'got the brand!',
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
