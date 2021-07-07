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
import datetime
import os
import traceback
import discord
from discord.ext import commands, menus
from jishaku.codeblocks import codeblock_converter
from jishaku.shell import ShellReader
from tabulate import tabulate
from dagbot.utils.conventionalpag import DaggyPaginatorClassic
from dagbot.utils.daggypag import DaggyPaginator


class TabulateData(menus.ListPageSource):
    def __init__(self, data, headers, title):
        super().__init__(data, per_page=7)
        self.title = title
        self.headers = headers

    async def format_page(self, menu, entries):
        headers = self.headers
        embed = discord.Embed(title=self.title)
        tab = tabulate(entries, headers, tablefmt="fancy_grid")
        embed.description = f"```{tab}\n```"
        return embed


class Developer(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot: Dagbot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def byebyebot(self, ctx: MyContext):
        await self.bot.session.close()
        await self.bot.pool.close()
        await ctx.send('Shutting Down Now <a:catroll:720695153601282068>')
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def reloadm(self,ctx: MyContext, *, opt_s: str):
        try:
            eval(f'__import__("importlib").reload(__import__("dagbot").{opt_s})')
            await ctx.send(f"successfully reloaded `dagbot.{opt_s}`")
        except Exception as exc:
            await ctx.send(f"Error reloading `dagbot.{opt_s}` with \n```\n{''.join(traceback.format_exception(type(exc), exc, exc.__traceback__, 1))}\n```")

    @commands.command()
    @commands.is_owner()
    async def announcement(self, ctx: MyContext):
        await ctx.send('Title for the embed')

        def check(message):
            return (ctx.author.id == message.author.id) and (
                    message.channel == ctx.channel)

        e_tit = await self.bot.wait_for('message', check=check)
        await ctx.send('Send me the embed content')
        e_desc = await self.bot.wait_for('message', check=check)
        embed = discord.Embed(
            title=e_tit.content,
            description=e_desc.content,
            color=ctx.guild.me.color)

        embed.set_author(name='Dagbot Dev Team',
                         icon_url="https://dagbot-is.the-be.st/logo.png")
        embed.add_field(
            name='Server Invite',
            value="[Join Now](https://discord.gg/5Y2ryNq)",
            inline=True)
        embed.add_field(
            name='Bot Invite',
            value="[Click me](https://discordapp.com/api/oauth2/authorize?"
                  "client_id=675589737372975124&permissions=378944&scope=bot)",
            inline=True)
        channel = self.bot.get_channel(681778906780532757)
        if isinstance(channel, discord.TextChannel):
            await channel.send('New update', embed=embed)

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx: MyContext, kwarg: int, *, status: str):
        if kwarg == 0:
            await ctx.send("1: Game\n2:Watching\n3.listening\n")
        elif kwarg == 1:
            await self.bot.change_presence(activity=discord.Game(name=status))
        elif kwarg == 2:
            activity = discord.Activity(
                name=status, type=discord.ActivityType.watching)
            await self.bot.change_presence(activity=activity)
        elif kwarg == 3:
            activity = discord.Activity(
                name=status, type=discord.ActivityType.listening)
            await self.bot.change_presence(activity=activity)

    @commands.command()
    @commands.is_owner()
    async def test_pagination_standard(self, ctx: MyContext, num: int = 5):
        embed_data = [discord.Embed(title=f"Page Number {i+1}", color=ctx.guild.me.color) for i in range(num)]
        pag = DaggyPaginatorClassic(ctx, embed_data)
        await ctx.send(embed=embed_data[0], view=pag)

    @commands.command()
    @commands.is_owner()
    async def test_pagination_custom(self, ctx: MyContext, num: int = 5):
        embed_data = [discord.Embed(title=f"Page Number {i+1}", color=ctx.guild.me.color) for i in range(num)]
        pag = DaggyPaginator(ctx, embed_data)
        await ctx.send(embed=embed_data[0], view=pag)

    @commands.command()
    @commands.is_owner()
    async def rejectsuggestion(self, ctx: MyContext, msg_id, *, reason):
        if str(ctx.author.id) == "491174779278065689":
            channel = self.bot.get_channel(676031268009410570)
            if not isinstance(channel, discord.TextChannel):
                return await ctx.send(":(")
            y = await channel.fetch_message(msg_id)
            oldemb = y.embeds[0]
            descrip = str(oldemb.description)
            newemb = discord.Embed(
                title="SUGGESTION REJECTED",
                description=descrip,
                color=ctx.guild.me.color)
            newemb.add_field(name="Reason", value=reason)
            await y.edit(embed=newemb)
        else:
            await ctx.send("Only Daggy1234 has this ability, sorry")

    @commands.command()
    @commands.is_owner()
    async def approvesuggestion(self, ctx: MyContext, msg_id):
        if str(ctx.author.id) == "491174779278065689":
            channel = self.bot.get_channel(676031268009410570)
            if not isinstance(channel, discord.TextChannel):
                return await ctx.send(":(")
            y = await channel.fetch_message(msg_id)
            oldemb = y.embeds[0]
            descrip = str(oldemb.description)
            newemb = discord.Embed(
                title="SUGGESTION APPROVED",
                description=descrip,
                color=ctx.guild.me.color)
            await y.edit(embed=newemb)
        else:
            await ctx.send("Only Daggy1234 has this ability, sorry")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: MyContext, *, extension: str):
        mst = ""
        if extension == '~':
            files = [('dagbot.extensions.' + f.replace('.py', '')) for f in
                     os.listdir('./dagbot/extensions') if f.endswith('.py')]
            for file in files:
                try:
                    self.bot.reload_extension(file)
                    mst += f"<a:giftick:734746863340748892> {file}\n"
                except Exception:
                    mst += f"<a:gifcross:734746864280404018> {file}\n"
        else:
            files = [(f.replace('.py', '')) for f in os.listdir(
                './dagbot/extensions') if f.endswith('.py')]
            if extension in files:
                try:
                    self.bot.reload_extension(f"dagbot.extensions.{extension}")
                    mst = f"<a:giftick:734746863340748892> {extension}\n\n" \
                          f"We successfully reloaded it!"
                except Exception as exc:
                    traceback_data = ''.join(
                        traceback.format_exception(
                            type(exc), exc, exc.__traceback__, 1))
                    mst = f"<a:gifcross:734746864280404018> {extension}\n" \
                          f"```py\n{traceback_data}\n```"
            else:
                return await ctx.send(
                    f"Extension {extension} could not be found")
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.description = mst
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: MyContext, *, extension: str):
        files = [(f.replace('.py', '')) for f in os.listdir(
            './dagbot/extensions') if f.endswith('.py')]
        if extension in files:
            try:
                self.bot.unload_extension(f"dagbot.extensions.{extension}")
                mst = f"<a:giftick:734746863340748892> {extension}\n\n" \
                      f"We successfully unloaded it!"
            except Exception as exc:
                traceback_data = ''.join(
                    traceback.format_exception(
                        type(exc), exc, exc.__traceback__, 1))
                mst = f"<a:gifcross:734746864280404018> {extension}\n`" \
                      f"``py\n{traceback_data}\n```"
        else:
            return await ctx.send(f"Extension {extension} could not be found")
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.description = mst
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: MyContext, *, extension: str):
        files = [(f.replace('.py', '')) for f in os.listdir(
            './dagbot/extensions') if f.endswith('.py')]
        if extension in files:
            try:
                self.bot.load_extension(f"dagbot.extensions.{extension}")
                mst = f"<a:giftick:734746863340748892> {extension}\n\n" \
                      f"We successfully loaded it!"
            except Exception as exc:
                traceback_data = ''.join(
                    traceback.format_exception(
                        type(exc), exc, exc.__traceback__, 1))
                mst = f"<a:gifcross:734746864280404018> {extension}\n" \
                      f"```py\n{traceback_data}\n```"
        else:
            return await ctx.send(f"Extension {extension} could not be found")
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.description = mst
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def socketstats(self, ctx: MyContext):
        # https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/stats.py
        delta = datetime.datetime.utcnow() - self.bot.launch_time
        minutes = delta.total_seconds() / 60
        total = len(self.bot.socket_stats)
        cpm = total / minutes

        tit = (
            f'Socket Stats ,{total} socket events observed ({cpm:.2f}/minute)')
        useage = {key: value for key, value in
                  sorted(self.bot.socket_stats.items(),
                         key=lambda item: item[1], reverse=True)}
        fl = [[key, val] for key, val in zip(useage.keys(), useage.values())]
        print(fl)
        tab_data = TabulateData(fl, ['Event', 'Occurences'], tit)
        pages = menus.MenuPages(
            source=TabulateData(fl, ['Event', 'Occurences'], tit),
            clear_reactions_after=True)
        return await pages.start(ctx)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def command_stats(self, ctx: MyContext):
        useage = {key: value for key, value in
                  sorted(self.bot.useage.items(), key=lambda item: item[1],
                         reverse=True)}
        columns = ['commands', 'useage']
        cc = self.bot.commands_called
        fl = [[key, val] for key, val in zip(useage.keys(), useage.values())]
        pages = menus.MenuPages(source=TabulateData(fl, columns, f'Command '
                                                                 f'Stats, '
                                                                 f'{cc}'),
                                clear_reactions_after=True)
        return await pages.start(ctx)

    @commands.command()
    @commands.is_owner()
    async def cleanup(self, ctx: MyContext, message_int: int = 100):
        async for message in ctx.channel.history(limit=message_int):
            if message.author == self.bot.user:
                await message.delete()

    @commands.command()
    @commands.is_owner()
    async def cache(self, ctx: MyContext):
        await self.bot.caching.cogcache()
        await self.bot.caching.prefixcache()
        await self.bot.caching.automemecache()
        await ctx.send("Cached Everything")

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx: MyContext, *, code: str):
        cog = self.bot.get_cog("Jishaku")
        if not cog:
            return await ctx.send("No jishaku cog")
        res = codeblock_converter(code)
        await cog.jsk_python(ctx, argument=res)

    @commands.command()
    @commands.is_owner()
    async def shell(self, ctx: MyContext, *, command: str):
        cog = self.bot.get_cog("Jishaku")
        if not cog:
            return await ctx.send("No jishaku cog")
        code = codeblock_converter(command)
        await cog.jsk_shell(ctx, argument=code)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dev_stats(self, ctx: MyContext):
        res = await self.bot.session.get(
            "https://dagbot-site.herokuapp.com/api/botstats",
            headers={"Token": self.bot.data["stats"]})
        our = await res.read()
        url = await self.bot.session.post("https://paste.rs/", data=our)
        t = await url.text()
        self.bot.logger.debug(t)
        await ctx.author.send(t)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def new_stats(self, ctx: MyContext):
        res = await self.bot.session.post(
            "https://dagbot-site.herokuapp.com/api/newstats",
            headers={"Token": self.bot.data["stats"]})
        return await ctx.send(f"Code: {res.status}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def neofetch(self, ctx: MyContext):

        l = []
        with ShellReader("neofetch --logo") as read:
            async for line in read:
                l.append(line)
        l.pop()
        mstr = ("\n".join(l)).rstrip()
        mstr = mstr.rstrip()
        mstrb = "\n"
        with ShellReader("neofetch --stdout") as read:
            async for line in read:
                mstrb += (line + "\n")
        mstrb += "\n"
        embed = discord.Embed(title="Neofetch")
        embed.description = f"```shell\n{mstr}\n```\n\n```shell\n{mstrb}\n```"
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Developer(bot))
