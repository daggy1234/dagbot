from contextlib import suppress

import discord
from discord.ext import commands
from utils.exceptions import NoImageFound, NoMemberFound
from validator_collection import checkers

member_converter = commands.MemberConverter()
emoji_converter = commands.EmojiConverter()


class UrlValidator:
    async def validate(self, url):
        return checkers.is_url(str(url))


class BetterMemberConverter(commands.Converter):
    async def convert(self, ctx, argument):
        with suppress(Exception):
            mem = await member_converter.convert(ctx, argument)
            return mem
        with suppress(Exception):
            mem = await commands.UserConverter().convert(ctx, argument)
            return mem
        with suppress(discord.HTTPException):
            mem = await ctx.bot.fetch_user(argument)
            return mem
        raise NoMemberFound(str(argument))


class ImageConverter(commands.Converter):
    async def convert(self, ctx, argument):
        with suppress(NoMemberFound):
            mem = await BetterMemberConverter().convert(ctx, argument)
            return(str(mem.avatar_url_as(static_format='png', size=1024)))
        with suppress(Exception):
            emoji = await emoji_converter.convert(ctx, str(argument))
            return(str(emoji.url))
        if ctx.message.attachments:
            with suppress(Exception):
                return ctx.message.attachments[0].url
        elif checkers.is_url(str(argument)):
            return str(argument)
        else:
            raise NoImageFound('')
