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
import os
import traceback

import discord
from discord.ext import commands


class Developer(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def byebyebot(self, ctx):
        await self.bot.session.close()
        await self.bot.pg_con.close()
        await ctx.send('Shutting Down Now <a:catroll:720695153601282068>')
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                'https://discordapp.com/api/webhooks/727546679439654953/H05HMXP7FyKrGz4YmhnI-8W_6L7jSzkqzpCsoWVDqxLi9VmKJf1WiKIbn8tOnGhI7imt',
                adapter=AsyncWebhookAdapter(session))
            await webhook.send('Dagbot is down')
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def announcement(self, ctx):
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
        webhook = Webhook.from_url(
            'https://discordapp.com/api/webhooks/706536494227259513/sssn-2bg6CFW-0P4EjysBgKuoeyzx7SbpvpclXfq83nUhkdMLdgHraNszh03Tufr0kNk',
            adapter=AsyncWebhookAdapter(
                self.bot.session))
        embed.set_author(name='Dagbot Dev Team',
                         icon_url="https://dagbot-is.the-be.st/logo.png")
        embed.add_field(
            name='Server Invite',
            value="[Join Now](https://discord.gg/5Y2ryNq)",
            inline=True)
        embed.add_field(
            name='Bot Invite',
            value="[Click me](https://discordapp.com/api/oauth2/authorize?client_id=675589737372975124&permissions=378944&scope=bot)",
            inline=True)
        await webhook.send('New update', embed=embed)

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, kwarg: int, *, status: str):
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
    async def rejectsuggestion(self, ctx, msg_id, *, reason):
        if str(ctx.author.id) == "491174779278065689":
            channel = self.bot.get_channel(676031268009410570)
            y = await channel.fetch_message(msg_id)
            oldemb = y.embeds[0]
            descrip = str(oldemb.description)
            oldtit = oldemb.title
            newemb = discord.Embed(
                title=f"SUGGESTION REJECTED",
                description=descrip,
                color=ctx.guild.me.color)
            newemb.add_field(name="Reason", value=reason)
            await y.edit(embed=newemb)
        else:
            await ctx.send("Only Daggy1234 has this ability, sorry")

    @commands.command()
    @commands.is_owner()
    async def approvesuggestion(self, ctx, msg_id):
        if str(ctx.author.id) == "491174779278065689":
            channel = self.bot.get_channel(676031268009410570)
            y = await channel.fetch_message(msg_id)
            oldemb = y.embeds[0]
            descrip = str(oldemb.description)
            oldtit = oldemb.title
            newemb = discord.Embed(
                title=f"SUGGESTION APPROVED",
                description=descrip,
                color=ctx.guild.me.color)
            await y.edit(embed=newemb)
        else:
            await ctx.send("Only Daggy1234 has this ability, sorry")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, extension: str):
        mst = ""
        if extension == '~':
            files = [('extensions.' + f.replace('.py', ''))
                     for f in os.listdir(r'.\dagbot\extensions') if f.endswith('.py')]
            for file in files:
                try:
                    self.bot.reload_extension(file)
                    mst += f"<a:giftick:734746863340748892> {file}\n"
                except BaseException:
                    mst += f"<a:gifcross:734746864280404018> {file}\n"
        else:
            files = [(f.replace('.py', '')) for f in os.listdir(
                r'.\dagbot\extensions') if f.endswith('.py')]
            if extension in files:
                try:
                    self.bot.reload_extension(f"extensions.{extension}")
                    mst = f"<a:giftick:734746863340748892> {extension}\n\nWe successfully reloaded it!"
                except Exception as exc:
                    traceback_data = ''.join(
                        traceback.format_exception(
                            type(exc), exc, exc.__traceback__, 1))
                    mst = f"<a:gifcross:734746864280404018> {extension}\n```py\n{traceback_data}\n```"
            else:
                return await ctx.send(f"Extension {extension} could not be found")
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.description = mst
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, extension: str):
        files = [(f.replace('.py', '')) for f in os.listdir(
            r'.\dagbot\extensions') if f.endswith('.py')]
        if extension in files:
            try:
                self.bot.unload_extension(f"extensions.{extension}")
                mst = f"<a:giftick:734746863340748892> {extension}\n\nWe successfully unloaded it!"
            except Exception as exc:
                traceback_data = ''.join(
                    traceback.format_exception(
                        type(exc), exc, exc.__traceback__, 1))
                mst = f"<a:gifcross:734746864280404018> {extension}\n```py\n{traceback_data}\n```"
        else:
            return await ctx.send(f"Extension {extension} could not be found")
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.description = mst
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, extension: str):
        files = [(f.replace('.py', '')) for f in os.listdir(
            r'.\dagbot\extensions') if f.endswith('.py')]
        if extension in files:
            try:
                self.bot.load_extension(f"extensions.{extension}")
                mst = f"<a:giftick:734746863340748892> {extension}\n\nWe successfully loaded it!"
            except Exception as exc:
                traceback_data = ''.join(
                    traceback.format_exception(
                        type(exc), exc, exc.__traceback__, 1))
                mst = f"<a:gifcross:734746864280404018> {extension}\n```py\n{traceback_data}\n```"
        else:
            return await ctx.send(f"Extension {extension} could not be found")
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.description = mst
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Developer(bot))
