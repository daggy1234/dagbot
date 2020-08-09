import discord
from discord.ext import commands


class settings(commands.Cog):
    """Commands Related to bot configuration"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def prefix(self, ctx):
        g_id = ctx.guild.id
        for e in self.bot.prefdict:
            if e["server_id"] == str(g_id):
                prefix = e["command_prefix"]
                break
        return await ctx.send(
            "Current Command Prefix is: `{}`\n Use prefix help for more commands".format(
                prefix
            )
        )

    @prefix.command()
    @commands.has_permissions(manage_guild=True)
    async def help(self, ctx):
        return await ctx.send(
            """`
    Welcome, Admin Perms are required
    prefix current: will show the current prefix
    prefix set <prefix> : will change the prefix
    prefix revert : wil get the original prefix of 'do '
    PLEASE USE CURRENT PREFIX UNTIL CHANGED WITH CONFIRMATION
    `"""
        )

    @prefix.command()
    @commands.has_permissions(manage_guild=True)
    async def set(self, ctx, prefix: str, space_after="n"):
        if space_after == "y":
            prefix = prefix + " "
        if "--" in prefix:
            return await ctx.send(
                "`--` is forbidden as it is a cyber security threat. Thank you for understanding."
            )
        else:
            g_id = ctx.guild.id
            await self.bot.pg_con.execute(
                """
        UPDATE prefixesandstuff
        SET command_prefix=$1
        WHERE server_id = $2;""",
                prefix, str(g_id)

            )
            await self.bot.caching.prefixcache()
            return await ctx.send("PREFIX UPDATED TO `{}`".format(prefix))

    @prefix.command()
    @commands.has_permissions(manage_guild=True)
    async def revert(self, ctx):
        g_id = ctx.guild.id
        await self.bot.pg_con.execute(
            """
    UPDATE prefixesandstuff
    SET command_prefix='do '
    WHERE server_id = $1;""",
            str(g_id)
        )

        await self.bot.caching.prefixcache()
        return await ctx.send("PREFIX UPDATED TO ```do ```")

    @prefix.command(aliases=["now"])
    async def current(self, ctx):
        id = ctx.guild.id
        for e in self.bot.prefdict:
            if e["server_id"] == str(id):
                prefix = e["command_prefix"]
                break
        return await ctx.send("Current Command Prefix is: ```{}```".format(prefix))

    @commands.group(invoke_without_command=True,aliases=['cogs'])
    async def cog(self, ctx):
        embed = discord.Embed(title="List Of cogs",color=ctx.guild.me.color)
        l = '\n'.join(self.bot.coglist)
        embed.description = l
        return await ctx.send("Please use cog help to get started!",embed=embed)

    @cog.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, *, cog):
        if str(cog) in self.bot.coglist:
            g_id = str(ctx.guild.id)
            await self.bot.pg_con.execute(
                f"""
            UPDATE cogpreferences
            SET {cog}='y'
            WHERE serverid = $1""", str(g_id))

            await self.bot.caching.cogcache()
            return await ctx.send(f"I have enabled the cog `{cog}` for this server")

        else:
            return await ctx.send("The cog you have entered does not exist")

    @cog.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx, *, cog):
        if str(cog) in self.bot.coglist:
            g_id = str(ctx.guild.id)
            await self.bot.pg_con.execute(
                f"""
            UPDATE cogpreferences
            SET {cog}='n'
            WHERE serverid = $1""", g_id)
            await self.bot.caching.cogcache()
            return await ctx.send(f"I have disabled the cog `{cog}` for this server.")

        else:
            return await ctx.send("The cog you have entered does not exist")

    @cog.command()
    async def status(self, ctx):
        id = ctx.guild.id
        embed = discord.Embed(
            title="COG STATUS FOR THIS SERVER", color=ctx.guild.me.color,
        )
        mstr = ""
        for c in self.bot.cogdata:
            if str(c["serverid"]) == str(id):
                for e in self.bot.coglist:
                    if e != "Jishaku" and e != "settings" and e != "Help":
                        if c[e]:
                            kwrd = "<:enableonx:723926397869097072><:enableont:723926397835280525>"
                        else:
                            kwrd = "<:disableonx:723926397642473534><:disableont:723926397784948809>"
                        mstr = mstr + "\n" + f"{kwrd} | {e}"
        embed.description = mstr
        return await ctx.send(embed=embed)

    @cog.command()
    async def help(self, ctx):
        return await ctx.send(
            """
        Cog Commands:
        A cog is a command category, you can enable or disable cogs and all of the commands inside them. Use the help menu to see all the available cogs. NOTE Meta and Help cogs cannot be disabled.
        `cog enable <cog> `: enables the cog to be used
        `cog disable <cog> `: disabled the cog
        `cog status <cog>`: shows teh status on wether a cog is enabled or disabled"""
        )


def setup(bot):
    bot.add_cog(settings(bot))
