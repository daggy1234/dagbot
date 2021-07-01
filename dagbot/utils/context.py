from __future__ import annotations
from typing import Union, Optional, TYPE_CHECKING
import discord
from discord.ext import commands
if TYPE_CHECKING:
    from dagbot.bot import Dagbot


class MyContext(commands.Context):

    bot: Dagbot
    guild: discord.Guild
    authot: discord.Member

    async def send(self,         
        content: Optional[str] = None,
        *,
        tts: bool = None,
        embed: discord.Embed = None,
        file: discord.File = None,
        delete_after: float = None,
        nonce: Union[str, int] = None,
        allowed_mentions: discord.AllowedMentions = None,
        reference: Union[discord.Message, discord.MessageReference] = None,
        mention_author: bool = None,
        view: discord.ui.View = None,
):
        bot = self.bot

        if content:
            for key, val in bot.data.items():
                if key not in ["imgflipuser", "database"]:
                    content = content.replace(val, f"[ Omitted {key} ]")
        else:
            content = ""
        if embed:
            desc = embed.description
            if desc:
                for key, val in bot.data.items():
                    if key not in ["imgflipuser", "database"]:
                        desc = desc.replace(val, f"[ Ommited {key}]")
                embed.description = desc
            embed.color = self.guild.me.color
            if len(embed) > 2048:
                return await super().send("This embed is a little too large "
                                          "to send.")
        if len(content) > 2000:
            return await super().send("Little long there woul you like me to "
                                      "upload this?")

        #typeignore
        return await super().send(content, file=file, embed=embed, 
                                  delete_after=delete_after, nonce=nonce,
                                  allowed_mentions=allowed_mentions, tts=tts, view=view)

    async def safe_send(self, yes):
        await super().send("Yes this method is cool")
