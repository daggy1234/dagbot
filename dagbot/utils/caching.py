class caching:
    def __init__(self, bot):
        print("will cache")
        self.bot = bot

    async def prefixcache(self):
        self.bot.prefdict = await self.bot.pg_con.fetch(
            """
    SELECT server_id,command_prefix FROM prefixesandstuff
    """
        )

    async def cogcache(self):
        self.bot.cogdata = await self.bot.pg_con.fetch(
            """
    SELECT * FROM cogpreferences;"""
        )

    async def getkeydict(self):
        wedit = self.bot.cogs
        keylist = []
        for key in wedit.keys():
            cog = self.bot.get_cog(key)
            if len(cog.get_commands(
            )) > 1 and cog.qualified_name != 'Jishaku' and cog.qualified_name != 'help' and cog.qualified_name != 'Developer':
                keylist.append(key)
        self.bot.coglist = keylist
