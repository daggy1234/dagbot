class Caching:
    def __init__(self, bot):
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
        wedit = self.bot.cogs
        keylist = []
        for key in wedit.keys():
            cog = self.bot.get_cog(key)
            if len(cog.get_commands()) > 1 \
                    and cog.qualified_name != 'Jishaku' \
                    and cog.qualified_name.lower() != 'help' \
                    and cog.qualified_name != 'Developer':
                keylist.append(key.lower())
        self.bot.coglist = keylist
