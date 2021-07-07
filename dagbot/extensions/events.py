from contextlib import suppress

import discord
from discord import Webhook
from discord.ext import commands


class EventHandler(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            ctx = await self.bot.get_context(after)
            await self.bot.invoke(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        g_id = message.guild.id
        prefix = "@Dagbot (run repair to fix. Guild is broken)"
        for e in self.bot.prefdict:
            if e["server_id"] == str(g_id):
                prefix = e["command_prefix"]
                break
        ctx = await self.bot.get_context(message)
        if not ctx.valid and self.bot.user in message.mentions:
            embed = discord.Embed(
                title="You hit me up?",
                description=f"""
        My Prefix for this server is: `{prefix}`
        Use the help command to get smart enough to use me: `{prefix}help` """,
                color=message.guild.me.color,
            )
            embed.add_field(
                name="Support Server",
                value="[Invite Link](https://discord.gg/grGkdeS)"
            )
            embed.add_field(
                name="Invite Link",
                value="[Click me](https://discordapp.com/api/oauth2/"
                      "authorize?client_id=675589737372975124&permissions="
                      "378944&scope=bot)",
            )
            await channel.send(embed=embed)
        # await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        g_id = guild.id
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    """
            INSERT INTO prefixesandstuff (on_message_perm,
                                        server_id,
                                        command_prefix)
            VALUES (True,$1,'do ');""",
                    str(g_id)
                )
                await connection.execute(
                    """
                INSERT INTO cogpreferences
                VALUES($1,'y','y','y','y','y','y','y','y','y','y','y','y');""",
                    str(g_id))
                del_query = """
                    DELETE FROM automeme WHERE server_id = $1;
                    """
                await connection.execute(del_query, g_id)
        await self.bot.caching.prefixcache()
        await self.bot.caching.automemecache()
        await self.bot.caching.cogcache()
        embed = discord.Embed(
            description=f"Joined guild {guild.name} [{guild.id}]",
            color=guild.me.color)
        embed.set_thumbnail(url=guild.icon_url_as(static_format="png"))
        embed.add_field(
            name="**Members**",  # Basic stats about the guild
            value=f"""**Total:** {guild.member_count}\n"
**Owner: ** {guild.owner}\n""",
            inline=False,
        )
        with suppress(Exception):
            # Tries to disclose who added the bot
            added_event = None
            async for thing in guild.audit_logs(limit=100):
                if thing.action == discord.AuditLogAction.bot_add:
                    added_event = thing
                    break
            if added_event:
                embed.add_field(name="Added By", value=added_event.user)

        webhook = Webhook.from_url(
            self.bot.data['guildlog'],
            session=self.bot.session)
        await webhook.send(
            f"We have  reached our **{len(self.bot.guilds)}th** server ",
            embed=embed, username='Dagbot Guilds')

        message = """
Thank you for adding Dagbot to your server!
The defualt prefix is `do ` but you can change this by using the \
`prefix set {prefix}` command! [see prefix help]
You can also @Dagbot to use commands.
The bot is modular and you can enable/disable command categories!
Check `cog help` to learn more.
For any help join our support server!

If there is an error with the bot try running the \
`repair` command that should fix everything!
Run `@dagbotrepair`

**server**: https://discord.gg/grGkdeS
**Website**: https://dagbot.daggy.tech
**Feedback**: https://dagbot.daggy.tech/feedback
"""
        try:
            await guild.system_channel.send(message)
        except Exception:
            for channel in guild.channels:
                try:
                    await channel.send(message)
                    break
                except Exception:
                    continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        g_id = str(guild.id)
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
        await self.bot.caching.prefixcache()
        await self.bot.caching.cogcache()
        self.bot.logger.warn("LEFT A GUILD")

    @commands.Cog.listener()
    async def on_socket_response(self, message):
        if not (stat := message.get('t')):
            try:
                self.bot.socket_stats['undocumented'] += 1
            except KeyError:
                self.bot.socket_stats['undocumented'] = 1
        try:
            self.bot.socket_stats[stat] += 1
        except KeyError:
            self.bot.socket_stats[stat] = 1


def setup(bot):
    bot.add_cog(EventHandler(bot))
