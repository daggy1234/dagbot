import codecs
import inspect
import os
import pathlib
import platform
from datetime import datetime

import discord
from discord.ext import commands


# from ..utils.converters import BetterMemberConverter
# from ..utils.exceptions import NoMemberFound


def linecount():
    total = 0
    file_amount = 0
    for path, subdirs, files in os.walk("."):
        for name in files:
            if name.endswith(".py"):
                file_amount += 1
                with codecs.open(
                        "./" + str(pathlib.PurePath(path, name)), "r", "utf-8"
                ) as f:
                    for i, l_c in enumerate(f):
                        stripped = l_c.strip()
                        if (stripped.startswith("#") or len(stripped) == 0):
                            pass
                        else:
                            total += 1
    return (
        f"I am made of {total:,} lines of Python, spread across  \
        {file_amount:,} files!"
    )


class misc(commands.Cog):
    """An assorted bag of ever changing commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sugg", "idea"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def suggest(self, ctx, *, suggest):
        guild = ctx.guild
        fro = guild.name
        auth = ctx.author.display_name
        embed = discord.Embed(
            title="DAGBOT SUGGESTION ADDED",
            description=f"```yaml\n{suggest}\n```\n**\
            FROM:***{auth}\n**SERVER:**{fro}",
            color=ctx.guild.me.color,
        )
        embed.add_field(
            name="SENT",
            value="Your SUGGESTION has been added to the Support server"
        )
        embed.add_field(
            name="Support Server",
            value="[Join Now](https://discord.gg/5Y2ryNq)"
        )
        embed.set_footer(text="id")
        channel = self.bot.get_channel(676031268009410570)
        msg = await channel.send(embed=embed)
        return await ctx.send(embed=embed)
        await msg.add_reaction("\U00002705")
        await msg.add_reaction("\U0000274c")

    @commands.command(aliases=["error", "problem"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def bug(self, ctx, *, bug):
        guild = ctx.guild
        fro = guild.name
        auth = ctx.author.display_name
        embed = discord.Embed(
            title="DAGBOT BUG REPORTED",
            description=f"```http\n{bug}\n```\n**\
            FROM:***{auth}\n**SERVER:**{fro}",
            color=ctx.guild.me.color,
        )
        embed.add_field(
            name="SENT",
            value="Your error has been sent to my creator's bug channel"
        )
        embed.add_field(
            name="Support Server",
            value="[Join Now](https://discord.gg/5Y2ryNq)"
        )
        channel = self.bot.get_channel(682199468375932928)
        await channel.send(embed=embed)
        return await ctx.send(embed=embed)

    # @commands.command()
    # async def serverinfo(self, ctx):
    #     online = len(
    #         [
    #             member
    #             for member in ctx.guild.members
    #             if member.status == discord.Status.online
    #         ]
    #     )
    #     offline = len(
    #         [
    #             member
    #             for member in ctx.guild.members
    #             if member.status == discord.Status.offline
    #         ]
    #     )
    #     idle = len(
    #         [
    #             member
    #             for member in ctx.guild.members
    #             if member.status == discord.Status.idle
    #         ]
    #     )
    #     dnd = len(
    #         [
    #             member
    #             for member in ctx.guild.members
    #             if member.status == discord.Status.dnd
    #         ]
    #     )
    #     botno = len(
    #         [member for member in ctx.guild.members if member.bot is True])
    #     guild = ctx.guild
    #     emojis = [emoji for emoji in ctx.guild.emojis]
    #     em_list = []
    #     for emoji in emojis:
    #         em_list.append(str(emoji))
    # text_channels = [text_channel for text_channel in guild.text_channels]
    #     voice_channels = [
    #         voice_channel for voice_channel in guild.voice_channels]
    #     categories = [category for category in guild.categories]
    #     emojis = [emoji for emoji in guild.emojis]
    #     region = f"{str(guild.region)}"
    #     roles = [role for role in ctx.guild.roles]
    #     role_list = " ".join(
    #         role.mention for role in roles[::-1][:10] if
    #         role.id != ctx.guild.id
    #     )
    #     embed = discord.Embed(
    #         colour=ctx.guild.me.color,
    #         title=f"{guild}",
    #  description=f"**Owner:** {ctx.guild.owner.mention}\n**Region:** \
    #  {region}\n**Guild created**: \
    #  {humanize.naturaltime(datetime.utcnow() - ctx.guild.created_at)}",
    #     )
    #     embed.set_thumbnail(url=guild.icon_url)
    #     if len(roles) > 10:
    #         msg = "Top 10 roles"
    #     else:
    #         msg = "Roles"
    #     filstr = "█"
    #     blankstr = "░"
    #     blankchar = "\u2000"
    #     boosts = int(guild.premium_subscription_count)
    #     if boosts > 30:
    #         boostcount = 30
    #     else:
    #         boostcount = boosts
    #
    #     bfrac = int((boostcount / 30) * 25)
    #     bar = f"{boosts} | `{filstr * bfrac}{blankchar * (25 - bfrac)}` | 30"
    #
    #     embed.add_field(
    #         name="Channels",
    #     value=f"<:category:724330131421659206>: \
    #     **{humanize.intcomma(len(categories))}**\n\
    #     <:textchannel:724637677395116072>: \
    #     **{humanize.intcomma(len(text_channels))}**\
    #     \n<:voicechannel:724637677130875001>: \
    #     **{humanize.intcomma(len(voice_channels))}**",
    #         inline=False,
    #     )
    #     embed.add_field(
    #         name="<:ppl:724330131233177632> Members",
    #         value=f"<:online:724328584621064193>: \
    #         **{humanize.intcomma(online)}**\n<:offline:724328584751349903>: \
    #         **{humanize.intcomma(offline)}**\n<:dnd:724328585078243438>: \
    #         **{humanize.intcomma(dnd)}**\n<:idle:724328584893956097>: \
    #         **{humanize.intcomma(idle)}**",
    #     )
    #     embed.add_field(
    #         name="<:bot:724330131426115674> Bots",
    #         value=f"**{humanize.intcomma(botno)}**",
    #     )
    #     embed.add_field(
    #         name="boosts",
    #         value=f"Level {guild.premium_tier}\n\
    #         {guild.premium_subscription_count} boosts\n{bar}",
    #         inline=False,
    #     )
    #     embed.add_field(name=f"{msg} (Total {len(roles)})", value=role_list)
    #     embed.add_field(
    #         name=f"Emojis (Total {len(emojis)})",
    #         value=" • ".join(em_list[:24]),
    #         inline=False,
    #     )
    #     return await ctx.send(embed=embed)

    # @commands.command(aliases=['ui'])
    # async def userinfo(self, ctx, user=None):
    #     sl = {
    #         "online": "<:online:724328584621064193>",
    #         "offline": "<:offline:724328584751349903>",
    #         "idle": "<:idle:724328584893956097>",
    #         "dnd": "<:dnd:724328585078243438>",
    #     }
    #
    #     mlsl = {
    #         "online": "\U0001f4f1",
    #         "offline": "\u200b",
    #         "idle": "\U0001f4f1",
    #         "dnd": "\U0001f4f1",
    #     }
    #
    #     wlsl = {"online": "🌐", "offline": "\u200b", "idle": "🌐", "dnd": "🌐"}
    #     # 🌐
    #
    #     dlsl = {
    #         "online": ":desktop:",
    #         "offline": "\u200b",
    #         "idle": ":desktop:",
    #         "dnd": ":desktop:",
    #     }
    #     if user is None:
    #         user = ctx.author
    #     else:
    #         user = await BetterMemberConverter().convert(ctx, user)
    #     badges = {
    #         "staff": "<:staff:724588086318596137>",
    #         "partner": "<:partner:724588086461202442>",
    #         "hypesquad": "<:hypesquadevents:724328584789098639>",
    #         "hypesquad_balance": "<:hypesquadbalance:724328585166454845>",
    #         "hypesquad_bravery": "<:hypesquadbravery:724328585040625667>",
    #         "hypesquad_brilliance": "<:hypesquadbrilliance:724328585363456070>",
    #         "bug_hunter": "<:bughunt:724588087052861531>",
    #         "bug_hunter_level_2": "<:bug2:699986097694048327>",
    #         "verified_bot_developer": "<:verifiedbotdev:724328584872984607>",
    #         "early_supporter": "<:earlysupporter:724588086646014034>",
    #     }
    #
    #     if user.bot:
    #         botthing = "<:bot:724330131426115674>"
    #     else:
    #         botthing = "\u0020"
    #     status_list = (
    #             f"{sl[str(user.status)]}\
    #             {mlsl[str(user.mobile_status)]}{wlsl[str(user.web_status)]}\
    #             {dlsl[str(user.desktop_status)]}"
    #             + botthing
    #     )
    #     embed = discord.Embed(
    #         title=f"{user.display_name}#{user.discriminator}",
    #         color=ctx.guild.me.color)
    #     realname = user.name + "#" + user.discriminator
    #     description = f"Original Name: {realname}\nJoined guild: \
    #     **{humanize.naturaltime(datetime.utcnow() - user.joined_at)}**\
    #     \nCreated account: \
    #
    #     **{humanize.naturaltime(datetime.utcnow() - user.created_at)}** "
    #     flags = [
    #         flag for flag, value in dict(user.public_flags).items() if
    #         value is True
    #     ]
    #     flagstr = ""
    #     for badge in badges.keys():
    #         if badge in flags:
    #             flagstr += f" {badges[badge]} "
    #     n = False
    #     if user.is_avatar_animated():
    #         n = True
    #     elif user.discriminator == '#0001':
    #         n = True
    #     else:
    #         for guild in self.bot.guilds:
    #             if user in guild.members:
    #                 if guild.get_member(user.id).premium_since is not None:
    #                     n = True
    #
    #     if n:
    #         flagstr += f" <:nitro:724328585418113134>"
    #     if len(flagstr) != 0:
    #         embed.add_field(name="Badges", value=flagstr)
    #     embed.add_field(name="status", value=status_list, inline=False)
    #     if len(description) != 0:
    #         embed.add_field(name="stats", value=description, inline=False)
    #
    #     # add badges
    #     try:
    #         mst = ""
    #         for a in user.activities:
    #             if isinstance(a, discord.Spotify):
    #                 activity = "Listening to **Spotify**"
    #             elif isinstance(a, discord.CustomActivity):
    #                 emoji = ""
    #                 if a.emoji:
    #                     if a.emoji.is_custom_emoji() and ctx.bot.get_emoji(
    #                             a.emoji.id) == False:
    #                         emoji = "<:crosss:720924220258779227>"
    #                     else:
    #                         emoji = a.emoji
    #                 activity = f'{emoji} {a.name or ""}'
    #             else:
    #                 try:
    #                     st = str(act.type).replace('ActivityType.', '')
    #                     activity = ((st + ' ' + act.name).title() + '\n')
    #                 except:
    #                     activity = ''
    #
    #             mst += activity + "\n"
    #
    #         if len(mst) != 0:
    #             embed.add_field(name="Activity", value=mst, inline=False)
    #     except BaseException:
    #         pass
    #     embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
    #     return await ctx.send(embed=embed)
    #
    # @commands.command(aliases=['spot'])
    # async def spotify(self, ctx, *, user=None):
    #     if user is None:
    #         user = ctx.author
    #     else:
    #         try:
    #             user = await commands.MemberConverter().convert(ctx, user)
    #         except BaseException:
    #             raise NoMemberFound(user)
    #     activities = user.activities
    #     try:
    #         act = [
    #             activity for activity in activities if isinstance(
    #                 activity, discord.Spotify)][0]
    #     except IndexError:
    #         return await ctx.send('No spotify was detected')
    #     start = humanize.naturaltime(datetime.utcnow() - act.created_at)
    #     print(start)
    #     name = act.title
    #     art = " ".join(act.artists)
    #     album = act.album
    #     duration = round(((act.end - act.start).total_seconds() / 60), 2)
    #     minsecdur = time.strftime(
    #         "%M:%S", time.gmtime(
    #             (act.end - act.start).total_seconds()))
    #     current = round(
    #         ((datetime.utcnow() - act.start).total_seconds() / 60), 2)
    #     minseccur = time.strftime("%M:%S", time.gmtime(
    #         (datetime.utcnow() - act.start).total_seconds()))
    #     embed = discord.Embed(color=ctx.guild.me.color)
    #     embed.set_author(
    #         name=user.display_name,
    #         icon_url='https://netsbar.com/wp-content/uploads/2018/10/Spotify_Icon.png')
    #     embed.description = f"Listening To  [**{name}**]\
    # (https://open.spotify.com/track/{act.track_id})"
    #     embed.add_field(name="Artist", value=art, inline=True)
    #     embed.add_field(name="Album", value=album, inline=True)
    #     embed.set_thumbnail(url=act.album_cover_url)
    #     embed.add_field(name="Started Listening", value=start, inline=True)
    #     pcent = int((current / duration) * 25)
    #     # old bar: █ ░
    #     pbar = f"`{minseccur}`| {(pcent - 1) * '─'}⚪️{(25 - pcent) * '─'} | \
    # `{minsecdur}`"
    #     embed.add_field(name="Progress", value=pbar)
    #     await ctx.send(embed=embed)
    #
    # @commands.command(aliases=['vsc'])
    # async def visualstudiocode(self, ctx, *, user=None):
    #     if user is None:
    #         user = ctx.author
    #     else:
    #         try:
    #             user = await commands.MemberConverter().convert(ctx, user)
    #         except BaseException:
    #             raise NoMemberFound(user)
    #     activities = user.activities
    #     try:
    #         l = []
    #         for activitiy in activities:
    #             try:
    #                 apid = activitiy.application_id
    #                 if apid == 383226320970055681:
    #                     l.append(activitiy)
    #             except BaseException:
    #                 continue
    #         act = l[0]
    #     except IndexError:
    #         return await ctx.send(
    #             'We could not detect VisualStudioCode Activity')
    #     file_url = act.large_image_url
    #     file_name = act.details
    #     vsclogo = act.small_image_url
    #     embed = discord.Embed(color=ctx.guild.me.color)
    #     embed.set_author(name=user.display_name, icon_url=vsclogo)
    #     embed.set_thumbnail(url=file_url)
    #     embed.description = file_name
    #     if file_name != "Idling":
    #         time = humanize.naturaltime(datetime.utcnow() - act.start)
    #         embed.add_field(name="Started", value=str(time))
    #         embed.add_field(name='details', value=str(act.state))
    #     return await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.add_field(
            name="Invite Link",
            value="[Click me](https://discordapp.com/api/oauth2/\
                authorize?client_id=675589737372975124&permissions=378944&\
                    scope=bot)"

        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.add_field(
            name="Support Server",
            value="[Invite Link](https://discord.gg/grGkdeS)",

        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def feedback(self, ctx):
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.add_field(
            name="Feedback Form",
            value="[Form](https://dagbot.daggy.tech/feedback)",

        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(
            title="About Dagbot",
            description="A ~~low effort and kinda useless~~ bot, \
            that does memes. With a bunch of hapahazardly thrown together \
            features dagbot should fullfill the need to entertain."
                        + linecount(), color=ctx.guild.me.color
        )
        channels = 0
        for guild in self.bot.guilds:
            for channel in guild.channels:
                channels += 1
        embed.add_field(
            name="Url's",
            value="[Invite Link]\
            (https://discordapp.com/api/oauth2/authorize?client_id=\
            675589737372975124&permissions=378944&scope=bot)\n[Support Server]\
            (https://discord.gg/grGkdeS)\n[API](https://dagpi.tk)\n[Website]\
            (https://dagbot.daggy.tech)\n[Source]\
            (https://github.com/Daggy1234/dagbot)",
        )
        embed.add_field(
            name="Stats",
            value=f"{len(self.bot.guilds)} servers\n{len(self.bot.users)} users \
                \n{channels} channels\n{len(self.bot.commands)} commands",
        )
        owner = self.bot.get_user(491174779278065689)
        embed.set_author(
            name=str(owner),
            icon_url=owner.avatar_url,
            url="https://github.com/Daggy1234/",
        )
        versions = f"<:python:737012280037736550> Python \
            {platform.python_version()}\n<:dpy:737012375747821650> \
                discord.py {discord.__version__}"
        embed.set_footer(text=versions)
        embed.timestamp = datetime.utcnow()
        return await ctx.send(embed=embed)

    @commands.command()
    async def credits(self, ctx):
        return await ctx.send(
            "Support Server my duded! Join and dm to get credit! \
                This command will come soon"
        )
        cmd = self.bot.get_command("support")
        await ctx.invoke(cmd)

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(color=ctx.guild.me.color)
        embed.add_field(
            name="Uptime", value=f"{days}d, {hours}h, {minutes}m, {seconds}s"
        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx, *, command: str = None):

        # This is inspired by R.danny source at
        # https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
        repo = "https://github.com/Daggy1234/dagbot"
        if command is None:
            return await ctx.send(repo)
        else:
            com = self.bot.get_command(command)
            if com is None:
                return await ctx.send(
                    'There is no command with that name. Maybe check the repo\n\
                        https://github.com/Daggy1234/dagbot')
            else:
                code = com.callback.__code__
                filename = code.co_filename
                lines, firstline = inspect.getsourcelines(code)
                location = os.path.relpath(filename).replace('\\', '/')
                final_url = f'{repo}/blob/master/{location}#L{firstline}-L \
                {firstline + len(lines) - 1}'
                return await ctx.send(final_url)


def setup(bot):
    bot.add_cog(misc(bot))
