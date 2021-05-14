import asyncio

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
            else:
                prefix = "@Dagbot (run repair to fix. Guild is broken)"
        return await ctx.send(
            "Current Command Prefix is: `{}`\n Use prefix help "
            "for more commands".format(
                prefix
            )
        )

    @prefix.command(name="help")
    @commands.has_permissions(manage_guild=True)
    async def prefix_help(self, ctx):
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
            prefix += " "
        if "--" in prefix:
            return await ctx.send(
                "`--` is forbidden as it is a cyber security threat. "
                "Thank you for understanding."
            )
        g_id = ctx.guild.id
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
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
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
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
        return await ctx.send(
            "Current Command Prefix is: ```{}```".format(prefix))

    @commands.group(invoke_without_command=True, aliases=['cogs'])
    async def cog(self, ctx):
        embed = discord.Embed(title="List Of cogs", color=ctx.guild.me.color)
        embed.description = '\n'.join(self.bot.coglist)
        return await ctx.send("Please use cog help to get started!",
                              embed=embed)

    @cog.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, *, cog):
        if str(cog) in self.bot.coglist:
            g_id = str(ctx.guild.id)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(
                        f"""
                    UPDATE cogpreferences
                    SET {cog}='y'
                    WHERE serverid = $1""", str(g_id))

            await self.bot.caching.cogcache()
            return await ctx.send(
                f"I have enabled the cog `{cog}` for this server")

        else:
            return await ctx.send("The cog you have entered does not exist")

    @cog.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx, *, cog):
        if str(cog) in self.bot.coglist:
            g_id = str(ctx.guild.id)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(
                        f"""
                    UPDATE cogpreferences
                    SET {cog}='n'
                    WHERE serverid = $1""", g_id)
            await self.bot.caching.cogcache()
            return await ctx.send(
                f"I have disabled the cog `{cog}` for this server.")

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
                    if e not in ["Jishaku", "settings", "Help"]:
                        if c[e]:
                            kwrd = "<:enableonx:723926397869097072>" \
                                   "<:enableont:723926397835280525>"
                        else:
                            kwrd = "<:disableonx:723926397642473534>" \
                                   "<:disableont:723926397784948809>"
                        mstr = mstr + "\n" + f"{kwrd} | {e}"
        embed.description = mstr
        return await ctx.send(embed=embed)

    @cog.command()
    async def help(self, ctx):
        return await ctx.send(
            """
        Cog Commands:
        A cog is a command category, you can enable or disable cogs and all
        of the commands inside them. Use the help menu to see all the available
         cogs. NOTE Meta and Help cogs cannot be disabled.
        `cog enable <cog> `: enables the cog to be used
        `cog disable <cog> `: disabled the cog
        `cog status <cog>`: shows teh status on wether a cog is enabled or
        disabled"""
        )

    @commands.group(invoke_without_command=True)
    async def automeme(self, ctx):
        await ctx.send("""
        This is the command class used for Dagbots automeme.
        Commands:
        `automeme setup`: initiates an interactive process to setup automeme
        `automeme delete`: deleted the automeme from this server
        `automeme disable`: keeps config but ensures it is not active.
        `automeme enable`: restarts a disabled automemed. does not create
        """)

    @automeme.command(name="delete")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def dagpi_delete(self, ctx):
        msg = await ctx.send("Are you SURE you want to DELETE Automeme")
        await msg.add_reaction('<a:giftick:734746863340748892>')

        # and reaction.author != ctx.author

        def check(reaction, user):
            # print('reaction')
            return reaction.message.id == msg.id and not user.bot and \
                   user.id == ctx.author.id and \
                   str(reaction.emoji) == '<a:giftick:734746863340748892>'

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     check=check, timeout=60.0)

        except asyncio.TimeoutError:
            return await ctx.send(
                'No response recieved aborting deleteion ')
        else:
            await ctx.send("Deleteing Automemer")
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    query = """
                    SELECT * FROM automeme WHERE server_id = $1;
                    """
                    data = await connection.fetch(query, ctx.guild.id)
                    try:
                        adap = discord.AsyncWebhookAdapter(self.bot.session)
                        hook = discord.Webhook.from_url(data[0]["webhook_url"],
                                                        adapter=adap)
                    except KeyError or IndexError:
                        return await ctx.send(
                            "Could not find a automemer for this"
                            "server. Please setup one first")
                    del_query = """
                    DELETE FROM automeme WHERE server_id = $1;
                    """
                    await connection.execute(del_query, ctx.guild.id)
            await self.bot.caching.automemecache()
            try:
                await hook.delete(reason="Automemer Deletion")
                return await ctx.send("Deleted the Webook")
            except discord.Forbidden or discord.HTTPException:
                return await ctx.send("Deleted webhok from database."
                                      "Can not delete webhook from discord"
                                      "Plase manually delete the webhook"
                                      "Error due to missing perms")

    @automeme.command(name="enable")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def enable_automeme(self, ctx):
        msg = await ctx.send("Are you SURE you want to Enable Automeme")
        await msg.add_reaction('<a:giftick:734746863340748892>')

        # and reaction.author != ctx.author

        def check(reaction, user):
            # print('reaction')
            return reaction.message.id == msg.id and not user.bot and \
                   user.id == ctx.author.id and \
                   str(reaction.emoji) == '<a:giftick:734746863340748892>'

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     check=check, timeout=60.0)

        except asyncio.TimeoutError:
            return await ctx.send(
                'No response recieved aborting enable')
        else:
            await ctx.send("Starting Automeme")
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    del_query = """
                         UPDATE automeme
                         SET active = 'y'
                         WHERE server_id = $1;
                        """
                    await connection.execute(del_query, ctx.guild.id)
            await self.bot.caching.automemecache()
            return await ctx.send("Automeme has been enabled. Mesmes should "
                                  "start soon!")

    @automeme.command(name="status")
    async def auomeme_status(self, ctx):
        for res in self.bot.automeme_data:
            if res["server_id"] == ctx.guild.id:
                channel = self.bot.get_channel(res["channel_id"])
                embed = discord.Embed(color=ctx.guild.me.color,
                                      title="AUTOMEME STATUS")
                embed.description = f"`Channel` : {channel.mention}\n" \
                                    f"`Category`: {channel.category}\n" \
                                    f"`Active`  : {res['active']}"
                return await ctx.send(embed=embed)

        return await ctx.send("No Automeme Setup yet. use `automeme setup`")

    @automeme.command(name="disable")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def disable_automeme(self, ctx):
        msg = await ctx.send("Are you SURE you want to Disable Automeme")
        await msg.add_reaction('<a:giftick:734746863340748892>')

        # and reaction.author != ctx.author

        def check(reaction, user):
            # print('reaction')
            return reaction.message.id == msg.id and not user.bot and \
                   user.id == ctx.author.id and \
                   str(reaction.emoji) == '<a:giftick:734746863340748892>'

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     check=check, timeout=60.0)

        except asyncio.TimeoutError:
            return await ctx.send(
                'No response recieved aborting disable')
        else:
            await ctx.send("Stopping Automeme")
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    del_query = """

                             UPDATE automeme
                             SET active = 'f'
                             WHERE server_id = $1;
                            """
                    await connection.execute(del_query, ctx.guild.id)
            await self.bot.caching.automemecache()
            return await ctx.send("Automeme has been disabled. Memes should "
                                  "start soon!")

    @automeme.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        await ctx.send(
            "Welcome to dagbot automeme. "
            "Have fresh memes sent periodically without typing the command.\n"
            "To Begin please enter the name/id/mention a channel in server\n"
            "This Channel will Contain the automemer")

        def check(message):
            return (
                    message.author == ctx.author
                    and message.channel == ctx.channel
                    and not message.author.bot
            )

        try:
            msg = await self.bot.wait_for("message", timeout=60.0,
                                          check=check)
        except asyncio.TimeoutError:
            return await ctx.send(
                "No Channel was provided. We need to be able to create a "
                "channel"
            )
        else:
            try:
                cont = (msg.content)
                channel = await commands.TextChannelConverter().convert(ctx,
                                                                        cont)
            except commands.ChannelNotFound or commands.BadArgument:
                return await ctx.send("Could not get a channel "
                                      "from your message. Please try again.")
            else:
                await ctx.send(f"Wil begin setting up automeme\nChannel INFO"
                               f"\n**name**:{str(channel)}\n**id**:"
                               f"{channel.id}\n**Categry**:{channel.category}")
                try:
                    byt = await self.bot.user.avatar_url.read()
                    hook = await channel.create_webhook(name="Dagbot Automeme",
                                                        avatar=byt,
                                                        reason="Dagbot "
                                                               "Automem Setup")
                    await ctx.send("Created Webhook")
                except discord.Forbidden or discord.HTTPException:
                    return await ctx.send("Dagbot needs the `create_webhook` "
                                          "permission to create the webhook. "
                                          "Please add this permission.")
                else:
                    async with self.bot.pool.acquire() as connection:
                        async with connection.transaction():
                            query = """
                            INSERT INTO automeme
                            VALUES ($1,$2,$3,'y');
                            """
                            await connection.execute(query,
                                                     ctx.guild.id,
                                                     channel.id,
                                                     hook.url)
                    await self.bot.caching.automemecache()
                    return await ctx.send("Created AUTOMEMER")

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def integrations(self, ctx):
        cmd_cog = self.bot.get_command("cog status")
        cmd_automeme = self.bot.get_command("automeme status")
        prefix = self.bot.get_command("prefix status")
        id = ctx.guild.id
        for e in self.bot.prefdict:
            if e["server_id"] == str(id):
                prefix = e["command_prefix"]
                break
            else:
                prefix = "@Dagbot (run repair to fix. Guild is broken)"
        embed = discord.Embed(
            title="You hit me up?",
            description=f"""
My Prefix for this server is: `{prefix}`
Use the help command to get smart enough to use me: `{prefix}help` """,
            color=ctx.guild.me.color,
        )
        embed.add_field(
            name="Support Server",
            value="[Invite Link](https://discord.gg/grGkdeS)"
        )
        embed.add_field(
            name="Invite Link",
            value="[Click me](https://discordapp.com/api/oauth2/authorize?"
                  "client_id=675589737372975124&permissions=378944&scope=bot)",
        )
        await ctx.send(embed=embed)
        await ctx.invoke(cmd_cog)
        await ctx.invoke(cmd_automeme)

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def repair(self, ctx):
        guild = ctx.guild
        g_id = str(guild.id)
        await ctx.send("Starting to delete all of the Data")
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    """
            DELETE FROM prefixesandstuff
            WHERE (server_id = $1) ;""", g_id)
                await connection.execute(
                    """
            DELETE FROM cogpreferences
            WHERE (serverid = $1) ;""", g_id)
                await ctx.send(
                    "Adding Data to the Database. New Configuration")
                await connection.execute(
                    """
        INSERT INTO prefixesandstuff (on_message_perm,server_id,command_prefix)
        VALUES (True,$1,'do ');""",
                    str(g_id)
                )
                await connection.execute(
                    """
                INSERT INTO cogpreferences
                VALUES($1,'y','y','y','y','y','y','y','y','y','y','y','y');""",
                    str(g_id))

        await ctx.send("Repopulating the Cache")
        await self.bot.caching.prefixcache()
        await self.bot.caching.cogcache()
        await ctx.send("Guild has been repaired. "
                       "For more issues join the support server")


def setup(bot):
    bot.add_cog(settings(bot))
