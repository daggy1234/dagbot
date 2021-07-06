from contextlib import suppress
from time import process_time

from discord import message, sticker
from dagbot.utils.context import MyContext

import discord
from typing import Any, Optional
from discord.ext import commands
from validator_collection import checkers

from dagbot.utils.exceptions import NoImageFound, NoMemberFound

member_converter = commands.UserConverter()
emoji_converter = commands.EmojiConverter()


class UrlValidator:
    async def validate(self, url):
        return checkers.is_url(str(url))


class BetterMemberConverter(commands.Converter):
    async def convert(self, ctx: MyContext, argument: Any) -> discord.User:
        with suppress(Exception):
            mem = await member_converter.convert(ctx, argument)
            ctx.bot.logger.info(mem)
            return mem
        with suppress(discord.HTTPException):
            mem = await ctx.bot.fetch_user(argument)
            return mem
        raise NoMemberFound(str(argument))


class ImageConverter(commands.Converter):



    async def process_msg(self, ctx: MyContext, message: discord.Message) -> str:

        if message.attachments and (len(message.attachments) > 0) and (message.attachments[0].height):
            with suppress(Exception):
                return message.attachments[0].url.replace(".webp", ".png")

        if len(message.stickers) >= 1:
            sticker_asset = message.stickers[0].image
            if sticker_asset:
                return sticker_asset.with_static_format("png").with_size(1024).url

        raise NoImageFound('')


    async def convert(self, ctx: MyContext, argument) -> str:

        message = ctx.message
        ref = message.reference
        ctx.bot.logger.info("Ready to convert gg")
        print("Converter is poggers")

        with suppress(NoMemberFound):
            mem = await BetterMemberConverter().convert(ctx, argument)
            print(mem)
            av = str(mem.avatar.with_static_format("png").with_size(1024).url)
            return av
        ctx.bot.logger.info("No member moment")
        with suppress(Exception):
            return await self.process_msg(ctx, message)
        ctx.bot.logger.info("Message sucked")
        with suppress(Exception):
            emoji = await emoji_converter.convert(ctx, str(argument))
            return (str(emoji.url))
        if checkers.is_url(str(argument)):
            return str(argument)
        if ref:
            with suppress(Exception):
                chan = ctx.bot.get_channel(ref.channel_id)
                if chan and isinstance(chan, discord.TextChannel):
                    msg = await chan.fetch_message(ref.message_id)
                    return await self.process_msg(ctx, msg)


        
        raise NoImageFound('')


class StaticImageConverter(commands.Converter):
    async def convert(self, ctx, argument):
        with suppress(NoMemberFound):
            mem = await BetterMemberConverter().convert(ctx, argument)
            av = str(mem.avatar.with_format("png").with_static_format("png").with_size(1024).url)
            return str(av)
        with suppress(Exception):
            emoji = await emoji_converter.convert(ctx, str(argument))
            return (str(emoji.url_as(format="png")))
        if ctx.message.attachments:
            with suppress(Exception):
                return ctx.message.attachments[0].url.replace(".webp", ".png")
        if checkers.is_url(str(argument)):
            return str(argument)
        if ctx.message.reference:
            with suppress(Exception):
                msg_ref = ctx.message.reference
                chan = ctx.bot.get_channel(msg_ref.channel_id)
                msg = await chan.fetch_message(msg_ref.message_id)
                return msg.attachments[0].url.replace(".webp", ".png")
        raise NoImageFound('')
