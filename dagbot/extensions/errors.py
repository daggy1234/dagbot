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
import random
import traceback

import asyncdagpi.exceptions as dex
import data.textdata as data
import discord
from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands
from sentry_sdk import capture_exception, configure_scope
from utils.exceptions import CustomError, NoImageFound, NoMemberFound


class ErrorHandler(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        ers = f"{error}"
        etype = type(error)
        trace = error.__traceback__
        verbosity = 4
        lines = traceback.format_exception(etype, error, trace, verbosity)
        traceback_text = "".join(lines)
        if hasattr(ctx.command, "on_error"):
            return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        ignored = (commands.CommandNotFound, commands.TooManyArguments)
        dagpibrok = (dex.APIError, dex.IncorrectToken, dex.RateLimited)

        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            rets = random.choice(data.missingargs)
            pr = error.param.name
            return await ctx.send(
                rets
                + f"\n\n.You need the parameter `{pr}` to make the command `{ctx.invoked_with}` work."
            )
        # elif isinstance(error,RuntimeError):
        #     bot.session = aiohttp.ClientSession()
        #     return await ctx.send('new sesh')
        elif isinstance(error, commands.MissingPermissions):
            rets = random.choice(data.missingperms)
            return await ctx.send(rets)
        elif isinstance(error, commands.MissingRole):
            return await ctx.send(f"NEED ROLE")
        elif isinstance(error, commands.CheckFailure):
            return print("CHECK FAIL")
        elif isinstance(error, commands.CommandOnCooldown):
            str = ctx.author.mention
            time = error.retry_after
            time = round(time, 2)
            rets = random.choice(data.cooldowncom)
            fst = rets + f" {time}s"
            return await ctx.send(fst)
        elif isinstance(error, commands.BotMissingPermissions):
            perms = ""
            for e in error.missing_perms:
                perms += f"{e}\n"
            embed = discord.Embed(
                title="Missing Perms",
                description=f"I need the following Permisisons to work!\n" + perms,
                color=ctx.guild.me.color
            )
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.MaxConcurrencyReached):
            times = error.number
            cat = error.per
            rets = random.choice(data.concur)
            st = rets + \
                f"\nIt can only be used {times} time per {cat} concurrently."
            st = st.replace("BucketType.", "")
            return await ctx.send(
                rets +
                f"\n\nIt can only be used {times} time per {cat} concurrently."
            )
        elif isinstance(error, commands.NotOwner):
            return await ctx.send("Only my daddy can do that")
        elif isinstance(error, commands.UnexpectedQuoteError):
            return await ctx.send(
                f"Why is there a sudden quote?`{error.quote}`\n Please fix and Try again"
            )
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            return await ctx.send(
                f"please match all of your quotes!`{error.close_quote}` was found dangling\n Please fix and Try again"
            )
        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            return await ctx.send(
                f"For the command {ctx.invoked_with}, please leave a space after the quote. Ex: `' `.\n Do not use {error.char}"
            )
        elif isinstance(error, commands.BadArgument):
            if "not found" in (ers):
                rest = random.choice(data.notfoundelist)
                await ctx.send(rest)
        else:
            capture_exception(error)
        if isinstance(error, commands.CommandInvokeError):
            error = getattr(error, "original", error)
            if isinstance(error, NoMemberFound):
                return await ctx.send((error))
            elif isinstance(error, NoImageFound):
                return await ctx.send((error))
            elif isinstance(error, dagpibrok):
                return await ctx.send('The API at https://dagpi.tk broke')
            elif isinstance(error, dex.FileTooLarge):
                return await ctx.send('The image your privided was too large to process')
            elif isinstance(error, dex.ImageUnaccesible):
                return await ctx.send('There was no image the bot could access at your url')
            else:
                name = ctx.author.display_name
                server = ctx.guild.name
                embed = discord.Embed(
                    title="Dagbot UNKOWN ERROR OCCURED",
                    description=f"```python\n{repr(error)}\n ```\nThe command {ctx.invoked_with} caused the error\n**Author:**{name}\n**Server:**{server}",
                    color=ctx.guild.me.color,
                )
                embed.add_field(
                    name="SENT",
                    value="Your error has been sent to my creator's bug channel",
                )
                embed.add_field(
                    name="Support Server", value="[Join Now](https://discord.gg/5Y2ryNq)"
                )
                nemb = discord.Embed(
                    title="Dagbot UNKOWN ERROR OCCURED",
                    description=f"```python\n{traceback_text}\n ```\nThe command {ctx.invoked_with} caused the error\n**Author:**{name}\n**Server:**{server}",
                    color=ctx.guild.me.color,
                )
                try:
                    webhook = Webhook.from_url(
                        self.bot.data['errorwebhook'],
                        adapter=AsyncWebhookAdapter(
                            self.bot.session))
                    await webhook.send('New Error', embed=nemb)
                except RuntimeError:
                    channel = self.bot.get_channel(682199468375932928)
                    await channel.send(embed=nemb)
                with configure_scope() as scope:
                    scope.user = {
                        "id": ctx.author.id,
                        "username": ctx.author.name}
                    scope.set_tag("message_id", ctx.message.id)
                    scope.set_tag("guild_id", ctx.guild.id)
                    scope.set_tag('guild_name', ctx.guild.name)
                    scope.set_tag("channel_id", ctx.channel.id)
                    scope.set_tag('channel_name', ctx.channel.name)
                capture_exception(error)
                await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_error(self, error, *args, **kwargs):
        capture_exception(error)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
