import asyncio
from contextlib import suppress

import discord
import difflib
from async_timeout import timeout
from discord.ext import commands
from discord.ext.commands import bot
from typing import List
from dagbot.utils.context import MyContext
import dagbot.data.textdata as data


class DagbotHelpView(discord.ui.View):

    def __init__(self, ctx: MyContext):
        super().__init__(timeout=400)

    async def process_callback(select: discord.ui.Select, interaction: discord.Interaction):
        DagbotHelp.cog_help_maker()
        print("")


class HelpSelect(discord.ui.Select):

    view: DagbotHelpView

    def __init__(self, *, options: List[discord.SelectOption]) -> None:
        super().__init__(placeholder="Dagbot Help Command",
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await self.view.process_callback(self, interaction)


class DagbotHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        ctx = self.context
        guild = ctx.guild
        g_id = guild.id
        for e in ctx.bot.prefdict:
            if e["server_id"] == str(g_id):
                prefix = e["command_prefix"]
                break
        embed = discord.Embed(color=guild.me.color)
        embed.set_author(
            icon_url=ctx.author.avatar_url,
            name="Dagot Help Command")
        embed.description = '''`[]` means that a parameter is optional\n`<>`
        means that a parameter is required\nYou can use do `help <command> \
help <category>` for help with specific commands or react with the
reactions below.'''
        cog_moji = []
        cog_list = []
        for record in ctx.bot.cogdata:
            if str(record["serverid"]) == str(g_id):
                for cog, state in zip(record.keys(), record.values()):
                    if cog != 'serverid' and state is True:
                        cog_list.append(cog)
                        em = data.emojilist[cog]
                        cog_moji.append(em)
                        embed.add_field(name=f"{cog} {em}", value='_')
        embed.add_field(name='help', value='-')
        cog_list.append('help')
        embed.add_field(name='settings', value='-')
        cog_list.append('settings')
        embed.add_field(name='prefix', value=f'`{prefix}`')
        emoji_list = [data.emojilist[cog] for cog in cog_list]
        msg = await ctx.send(embed=embed)
        for emoji in emoji_list:
            await msg.add_reaction(emoji)

        def check(reaction, user) -> bool:
            return str(reaction) in emoji_list \
                and reaction.message.channel == ctx.channel \
                and not user.bot and user == ctx.author
        try:
            async with timeout(300):
                while True:
                    try:
                        reaction, user = await ctx.bot.wait_for('reaction_add',
                                                                check=check,
                                                                timeout=20)
                    except asyncio.TimeoutError:
                        continue
                    else:

                        ind = emoji_list.index(str(reaction))

                        cog = cog_list[ind]
                        if cog == 'help':
                            await msg.edit(embed=embed)
                        else:

                            coginst = ctx.bot.get_cog(cog.lower())
                            if coginst is None:
                                continue
                            embd = await self.cog_help_maker(coginst, ctx)
                            embd.set_author(
                                icon_url=ctx.author.avatar_url,
                                name="Dagot Help Command")
                            await msg.edit(embed=embd)
        except BaseException:
            return

    @staticmethod
    async def cog_help_maker(cog: commands.Cog, ctx: MyContext) -> discord.Embed:
        sp = 15
        guild = ctx.guild
        g_id = guild.id
        for e in ctx.bot.prefdict:
            if e["server_id"] == str(g_id):
                prefix = e["command_prefix"]
                break

        cog_commands = cog.get_commands()
        cmlist = ""
        if len(cog_commands) == 0:
            return await ctx.send(
                "This cog doesn't have any commands for some reason.")
        # command.clean_params

        if cog.qualified_name == "animals":
            addi = "Self explanatory get facts or images! \n Try them and see"
        elif cog.qualified_name == "image":
            addi = "TRY THEM AND SEE, CANNOT EXPLAIN\n Please note `source` " \
                   "means you can attach an image, provide a url or mention " \
                   "someone\n `user` only accepts a member"
        else:
            addi = ""

        embed = discord.Embed(
            color=ctx.guild.me.color,
            title=f"{cog.qualified_name} help\n{addi}",
        )

        if cog.qualified_name == "memes":
            tmstr = 20
        elif cog.qualified_name == "settings":
            tmstr = 10
        else:
            tmstr = 30
        if ctx.author.id == 491174779278065689:
            comlist = [command for command in cog_commands]
        else:
            comlist = [
                command for command in cog_commands if not command.hidden]
        for command in comlist:
            sig = command.signature
            sig = sig.replace('[source]', '<source>')
            try:
                file = data.cmdhelp[f"{command}"]
            except BaseException:
                if cog.qualified_name in ["image", "animals"]:
                    des = ""
                else:
                    des = "No help just yet! We are working on it!"
            else:
                des = file
            toadd = f"○`{prefix}{command.name} {sig}`"
            sp = tmstr - len(toadd)
            spc = sp * "\u2000"
            cmlist = cmlist + toadd + f"{spc}{des}"
            cmlist += "\u200b 🞵\n" if isinstance(command,
                                                 commands.Group) else "\n"
        embed.description = cmlist
        embed.set_footer(
            text=f"🞵 means that the command listed is a Group. Use "
                 f"{prefix}help <group> for help with its subcommands."
        )

        return embed

    async def send_cog_help(self, cog):
        ctx = self.context
        r = False
        g_id = ctx.guild.id
        for record in ctx.bot.cogdata:
            if str(record["serverid"]) == str(g_id):
                for cogthing, state in zip(record.keys(), record.values()):
                    if cog.qualified_name == cogthing and state is True:
                        r = True
        if r:
            embed = await self.cog_help_maker(cog, ctx)
            return await ctx.send(embed=embed)
        else:
            return await ctx.send('The cog has been disabled in the server')

    async def send_group_help(self, group):
        ctx = self.context
        guild = ctx.guild
        ctx = self.context

        embed = discord.Embed(color=guild.me.color, )

        if group.signature:
            embed.title = f"{group.qualified_name} {group.signature}"
        else:
            embed.title = f"{group.qualified_name} group"
        try:
            hel = data.grouphelp[group.qualified_name]
        except BaseException:
            embed.description = (
                "We are in the process of adding help to this group.\n\n"
            )
        else:
            embed.description = hel

        return await ctx.send(embed=embed)

    async def bucket_type_processor(self, btype: commands.BucketType):
        if btype == commands.BucketType.user:
            return "user"
        elif btype == commands.BucketType.channel:
            return "guild"
        elif btype == commands.BucketType.guild:
            return "server"
        else:
            return str(btype)

    async def send_command_help(self, command):
        ctx = self.context
        guild = ctx.guild
        embed = discord.Embed(color=guild.me.color, )
        sig = command.signature
        sig = sig.replace('[source]', '<source>')
        embed.title = f"{command.name} {sig}"
        try:

            embed.description = data.cmdhelp[f"{command}"]
        except BaseException:
            embed.description = command.help or "No help just yet!"
        alis = command.aliases
        als = "none" if len(alis) == 0 else ', '.join(alis)
        embed.add_field(name="Aliases", value=als, inline=True)
        embed.add_field(
            name="Command Group",
            value=command.cog_name,
            inline=True)
        with suppress(AttributeError):
            cmd = command
            rate = cmd._buckets._cooldown.rate
            time = cmd._buckets._cooldown.per
            typ = await self.bucket_type_processor(cmd._buckets._cooldown.type)
            embed.add_field(
                name="Cooldowns",
                value=f"This command may be used {rate} times every {time}s "
                      f"per {typ}",
                inline=False)
        with suppress(AttributeError):
            cmd = command
            rate = cmd._max_concurrency.number
            typ = await self.bucket_type_processor(cmd._max_concurrency.per)
            embed.add_field(
                name="Concurrency",
                value=f"This command may be used only {rate}  per {typ}",
                inline=False)
        return await ctx.send(embed=embed)

    def command_not_found(self, string):
        ctx = self.context
        com = [command.qualified_name for command in ctx.bot.commands]
        matches = difflib.get_close_matches(string, com)
        base = f"No command named {string}\nDid you mean:\n"
        if len(matches) == 0:
            return f"No command named {string}"
        coms = "\n".join(f"`{match}`" for match in matches)
        return base + coms

    def get_destination(self):
        return self.context.channel

    async def send_error_message(self, error):
        ctx = self.context
        destination = self.get_destination()
        embed = discord.Embed(title="Help Error",
                              color=ctx.guild.me.color)
        embed.description = error
        await destination.send(embed=embed)


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = DagbotHelp()
        bot.help_command.cog = self

    @commands.command()
    async def default_help(self, ctx):
        await ctx.send(self._original_help_command)


def setup(bot):
    bot.add_cog(help(bot))
