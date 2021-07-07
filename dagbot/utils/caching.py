from __future__ import annotations
from typing import List, Mapping, Optional, TYPE_CHECKING

from discord.ext import commands
if TYPE_CHECKING:
    from dagbot.bot import Dagbot


class Caching:
    def __init__(self, bot: Dagbot):
        bot.logger.debug("WILL CACHE")
        self.bot = bot

    async def prefixcache(self):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                self.bot.prefdict = await connection.fetch(
                    """
            SELECT server_id,command_prefix FROM prefixesandstuff
            """
                )

    async def cogcache(self):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                self.bot.cogdata = await connection.fetch(
                    """
            SELECT * FROM cogpreferences;"""
                )

    async def automemecache(self):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                self.bot.automeme_data = await connection.fetch(

                    """
                    SELECT * FROM automeme;
                    """
                )

    async def getkeydict(self):
        wedit: Mapping[str, commands.Cog] = self.bot.cogs
        keylist: List[str] = []
        for key in wedit.keys():
            cog: Optional[commands.Cog] = self.bot.get_cog(key)
            if not cog:
                continue
            if len(cog.get_commands()) > 1 \
                    and cog.qualified_name != 'Jishaku' \
                    and cog.qualified_name.lower() != 'help' \
                    and cog.qualified_name != 'Developer':
                keylist.append(key.lower())
        self.bot.coglist = keylist
