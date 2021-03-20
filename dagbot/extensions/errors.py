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
import random
import traceback
import asyncdagpi.errors as dagpi_error
import discord
from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands
from sentry_sdk import capture_exception, configure_scope

import dagbot.data.textdata as data
from dagbot.utils.exceptions import NoImageFound, NoMemberFound


class ErrorHandler(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ers = f"{error}"
        traceback_text = "".join(traceback.format_exception(
            type(error), error, error.__traceback__, 4))
        if hasattr(ctx.command, "on_error"):
            return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        ignored = (commands.CommandNotFound, commands.TooManyArguments)
        dagpibrok = (dagpi_error.ApiError)
        dagpi_code_broke = (dagpi_error.Unauthorised, dagpi_error.RateLimited,
                            dagpi_error.InvalidFeature,
                            dagpi_error.Unauthorised)

        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            rets = random.choice(data.missingargs)
            pr = error.param.name
            return await ctx.send(
                rets
                + f"\n\n.You need the parameter `{pr}` to make the command "
                  f"`{ctx.invoked_with}` work."
            )
        # elif isinstance(error,RuntimeError):
        #     bot.session = aiohttp.ClientSession()
        #     return await ctx.send('new sesh')
        elif isinstance(error, commands.MissingPermissions):
            rets = random.choice(data.missingperms)
            return await ctx.send(rets)
        elif isinstance(error, commands.MissingRole):
            return await ctx.send("NEED ROLE")
        elif isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.CommandOnCooldown):
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
                description="I need the following Permisisons to work!"
                            "\n" + perms,
                color=ctx.guild.me.color
            )
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.MaxConcurrencyReached):
            times = error.number
            cat = error.per
            rets = random.choice(data.concur)
            st = rets + f"\nIt can only be used {times} " \
                        f"time per {cat} concurrently."
            st = st.replace("BucketType.", "")
            return await ctx.send(
                rets +
                f"\n\nIt can only be used {times} time per {cat} concurrently."
            )
        elif isinstance(error, commands.NotOwner):
            return await ctx.send("Only my daddy can do that")
        elif isinstance(error, commands.UnexpectedQuoteError):
            return await ctx.send(
                f"Why is there a sudden quote?`{error.quote}`\n "
                f"Please fix and Try again"
            )
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            return await ctx.send(
                f"please match all of your quotes!`{error.close_quote}` "
                f"was found dangling\n Please fix and Try again"
            )
        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            return await ctx.send(
                f"For the command {ctx.invoked_with}, "
                f"please leave a space after the quote. "
                f"Ex: `' `.\n Do not use {error.char}"
            )
        elif isinstance(error, commands.BadArgument):
            if "not found" in (ers):
                rest = random.choice(data.notfoundelist)
                await ctx.send(rest)
        print(repr(error))
        error = getattr(error, "original", error)
        if isinstance(error, NoMemberFound):
            return await ctx.send("Member found doesn't exist")
        elif isinstance(error, NoImageFound):
            return await ctx.send("No Valid Image was detected at your location\nPlease Specify a Valid Loaction Like\n```\n- Attachment (Add dummy text)\n- Member (ping or id)\n- Emoji (No standard emojis)\n- Url (Valid URL's only)\n```")
        elif isinstance(error, dagpibrok):
            return await ctx.send('The API at https://dagpi.xyz broke')
        elif isinstance(error, dagpi_code_broke):
            return await ctx.send('The code for dagpi broke')
        elif isinstance(error, dagpi_error.FileTooLarge):
            return await ctx.send(
                'The image your provided was too large to process')
        elif isinstance(error, dagpi_error.ImageUnaccesible):
            return await ctx.send(
                'There was no image the bot could access at your url' +
                str(error))
        else:
            name = ctx.author.display_name
            server = ctx.guild.name
            embed = discord.Embed(
                title="Dagbot UNKOWN ERROR OCCURED",
                description=f"```python\n{repr(error)}\n ```\n"
                            f"The command {ctx.invoked_with} caused the "
                            f"error\n**Author:**{name}\n"
                            f"**Server:**{server}",
                color=ctx.guild.me.color,
            )
            embed.add_field(
                name="SENT",
                value="Your error has been sent to the bug channel",
            )
            embed.add_field(
                name="Support Server",
                value="[Join Now](https://discord.gg/5Y2ryNq)"
            )
            nemb = discord.Embed(
                title="Dagbot UNKOWN ERROR OCCURED",
                description=f"```python\n{traceback_text}\n ```\n"
                            f"The command {ctx.invoked_with} caused the "
                            f"error\n"
                            f"**Author:**{name}\n**Server:**{server}",
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
                scope.set_tag('command', ctx.invoked_with)
            capture_exception(error)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_error(self, error, *args, **kwargs):
        capture_exception(error)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
