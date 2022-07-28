"""
    Dagbot is a discord meme bot that does nothing useful
    Copyright (C) 2020  Daggy1234

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from dagbot.bot import Dagbot
from dagbot.utils.context import MyContext

import discord
from discord.ext import commands

class animals(commands.Cog):
    """Animal facts and images"""

    def __init__(self, client: Dagbot):
        self.client = client
        self.image_animals = ["dog","cat","panda","red_panda","fox","birb","koala","kangaroo","racoon","whale","pikachu"]
        self.fact_animals = ["cat","dog"," koala","fox","bird","elephant","panda","racoon","kangaroo","giraffe","whale"]
        self.srapi = client.sr_api
        

        
        
        for animal in self.fact_animals:
            self.make_fn_fact(animal)

        for animal in self.image_animals:
            self.make_fn_image(animal)

    async def cog_check(self, ctx):
        g_id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if e["serverid"] == g_id:
                return bool(e["animals"])
    
    def make_fn_fact(self, animal: str):
        @commands.command(name=f"{animal}fact",
                          help=f"Get a random fact for {animal}")
        async def _command(_self, ctx: MyContext):
            await ctx.trigger_typing()
            fact = await self.srapi.get_fact(animal)
            embed = discord.Embed(
            title=f"{animal.title()} Fact!", description=fact, color=ctx.guild.me.color
            )
            return await ctx.send(embed=embed)

        _command.cog = self
        self.__cog_commands__ += (_command,) #type: ignore

    def make_fn_image(self, animal: str):
        @commands.command(name=f"{animal}",
                          help=f"Get a random image for {animal}")
        async def _command(_self, ctx: MyContext):
            await ctx.trigger_typing()
            y = await self.srapi.get_image(animal)
            embed = discord.Embed(
            title=f"Cute {animal.title()}!", color=ctx.guild.me.color
            )
            embed.set_image(url=y.url)
            return await ctx.send(embed=embed)

        _command.cog = self
        self.__cog_commands__ += (_command,) #type: ignore


async def setup(client: Dagbot):
    await client.add_cog(animals(client))