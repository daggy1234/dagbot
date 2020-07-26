import discord
from discord.ext import commands


class tags(commands.Cog):
    """Commands that can help quickly store and retrive data"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        id = str(ctx.guild.id)
        for e in self.bot.cogdata:
            if str(e["serverid"]) == str(id):
                if e["tags"]:
                    return True
                else:
                    return False

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, name):
        serverid = ctx.guild.id
        n = str(name).lower()
        if "--" in n:
            return await ctx.send(
                "`--` is forbidden as it is a cyber security threat. Thank you for understanding."
            )
        else:
            y = await self.bot.pg_con.fetch(
                """
        SELECT * FROM taglist
        WHERE (server = $1 AND name=$2);""",
                int(serverid), n
            )

            if len(y) == 0:
                return await ctx.send("Tag does not exist")
            else:
                return await ctx.send(y[0]["content"])
                uses = y[0]["uses"]
                uses += 1
                await self.bot.pg_con.execute(
                    """
        UPDATE taglist
        SET uses = $1
        WHERE (server = $2 AND name= $3);""",
                    int(uses), int(serverid), n
                )

    @tag.command(cooldown_after_parsing=True)
    async def info(self, ctx, *, name):
        guild = ctx.guild
        sid = ctx.guild.id
        if "--" in str(name).lower():
            return await ctx.send(
                "`--` is forbidden as it is a cyber security threat. Thank you for understanding."
            )
        else:
            y = await self.bot.pg_con.fetch(
                """
        SELECT * FROM taglist
        WHERE (name = $1 AND server = $2); """,
                str(name).lower(), int(sid)
            )

            if len(y) == 0:
                return await ctx.send("Tag does not exist")
            else:
                id = y[0]["author"]
                guy = self.bot.get_user(int(id))
                embed = discord.Embed(
                    title="Tag: {}".format(name), color=guild.me.color
                )
                embed.add_field(name="Creator", value=guy.mention)
                embed.add_field(name="Uses", value=y[0]["uses"])
                return await ctx.send(embed=embed)

    @tag.command(cooldown_after_parsing=True)
    async def rename(self, ctx, name, newname):
        id = ctx.author.id
        sid = ctx.guild.id
        newname = newname.lower()
        name = name.lower()
        if "--" in ((name) or (newname)):
            return await ctx.send(
                "`--` is forbidden as it is a cyber security threat. Thank you for understanding."
            )
        else:
            y = await self.bot.pg_con.fetch(
                """
        SELECT author FROM taglist
        WHERE (name = $1 AND server = $2); """,
                str(name), int(sid)
            )

            if len(y) == 0:
                return await ctx.send("Tag does not exist")
            elif (y[0]["author"]) == (id):
                await self.bot.pg_con.execute(
                    """
        UPDATE taglist
        SET name=$1
        WHERE (name = $2 AND server= $3)""",
                    str(newname), str(name), int(sid)
                )

                return await ctx.send("Tag {} is now tag {}".format(name, newname))
            else:
                return await ctx.send("Tag belongs to some one else, you cannot rename it")

    @tag.command(cooldown_after_parsing=True)
    async def update(self, ctx, name, *, content):
        id = ctx.author.id
        sid = ctx.guild.id
        name = name.lower()
        if "--" in (str(name) or str(content)):
            return await ctx.send(
                "`--` is forbidden as it is a cyber security threat. Thank you for understanding."
            )
        else:
            y = await self.bot.pg_con.fetch(
                """
        SELECT author FROM taglist
        WHERE (name = $1 AND server = $2); """,
                str(name), int(sid)
            )

            if len(y) == 0:
                return await ctx.send("Tag does not exist")
            elif (y[0]["author"]) == id:
                await self.bot.pg_con.execute(
                    """
        UPDATE taglist
        SET content=$1
        WHERE (name = $2 AND server=$3)""",
                    str(content), str(name), int(sid)
                )

                return await ctx.send("Changed the content of tag {}".format(name))
            else:
                return await ctx.send("Tag belongs to some one else, you cannot update it")

    @tag.command(cooldown_after_parsing=True)
    async def delete(self, ctx, *, name):
        id = ctx.author.id
        sid = ctx.guild.id
        name = name.lower()
        if "--" in str(name):
            return await ctx.send(
                "`--` is forbidden as it is a cyber security threat. Thank you for understanding."
            )
        else:
            y = await self.bot.pg_con.fetch(
                """
        SELECT author FROM taglist
        WHERE (name = $1 AND server = $2) ;""",
                str(name), int(sid)
            )

            if len(y) == 0:
                return await ctx.send("Tag does not exist")
            elif (str(y[0]["author"])) == id:
                await self.bot.pg_con.execute(
                    """
        DELETE FROM taglist
        WHERE name = $1;""",
                    str(name)
                )

                return await ctx.send("Tag deleted succesfully")
            else:
                return await ctx.send("Tag belongs to some one else, you cannot delete it")

    @tag.command(cooldown_after_parsing=True)
    async def help(self, ctx):
        return await ctx.send(
            """`
    tags:
    tag <name>: has the bot output the content of the tag
    tag create <name> <content>: stores tga with the content
    tag update <name> <content>: changes the content of tag
    tag rename <name> <newname>: changes the name of a tag
    tag delete <name> : deletes the tag only if you created it
    tag info <name>: gets the information about a particluar tag
    tag list <member>: gets a list of all of a members tags (mention them {sorry but ping})
    `"""
        )

    @tag.command(cooldown_after_parsing=True)
    async def list(self, ctx, member: discord.Member):
        id = member.id
        guild = ctx.guild
        sid = ctx.guild.id
        rep = await self.bot.pg_con.fetch(
            """
    SELECT * FROM taglist
    WHERE (server = $1 AND author = $2)""",
            sid, id
        )

        tlist = ""
        for r in rep:
            t = r["name"]
            tlist = tlist + "\n" + t
        if len(tlist) == 0:
            tlist = "None"
        embed = discord.Embed(
            title="{}'s Tags".format(str(member.name)),
            description=tlist,
            color=guild.me.color,
        )
        return await ctx.send(embed=embed)

    @tag.command(cooldown_after_parsing=True)
    @commands.cooldown(1, 5)
    async def create(self, ctx, name, *, content):
        serverid = ctx.guild.id
        guyid = ctx.author.id
        n = str(name)
        con = str(content)
        if "--" in (n or con):
            return await ctx.send(
                "`--` is forbidden as it is a cyber security threat. Thank you for understanding."
            )
        else:
            y = await self.bot.pg_con.fetch(
                """
        SELECT * FROM taglist
        WHERE (server = $1 AND name=$2);""",
                int(serverid), n

            )
            if len(y) == 0:
                await self.bot.pg_con.execute(
                    """
        INSERT INTO taglist (name,content,server,author,uses)
        VALUES($1,$2,$3,$4,0);""",
                    n, con, int(serverid), int(guyid)

                )
                return await ctx.send("Created Tag {}".format(n))
            else:
                return await ctx.send("Tag {} aldready exists on this server".format(n))

    @tag.error
    async def tage(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.send("gay")


def setup(bot):
    bot.add_cog(tags(bot))
