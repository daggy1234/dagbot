import random

from cryptography.fernet import Fernet

import discord
import sr_api
import zalgoify
from art import *
from discord.ext import commands
from owotext import OwO
from vaporwavely import vaporize

client = sr_api.Client()


def setup(client):
    client.add_cog(text(client))


class text(commands.Cog):
    """Fun ways to make your text more interesting"""

    def __init__(self, client):
        self.client = client
        self.uwu = OwO()
        self.cipher_suite = Fernet(Fernet.generate_key())

    async def cog_check(self, ctx):
        id = str(ctx.guild.id)
        for e in self.client.cogdata:
            if str(e["serverid"]) == str(id):
                if e["text"]:
                    return True
                else:
                    return False

    @commands.command(cooldown_after_parsing=True)
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        return await ctx.send(f"{t_rev}")

    @commands.command(cooldown_after_parsing=True)
    async def clapify(self, ctx, *, text):
        if len(text) > 1000:
            return await ctx.send("TOO LONG TO PROCESS")
        else:
            y = str(text)
            clist = []
            r = 0
            maste = ""
            for i in range(0, len(y)):
                if y[i] == " ":
                    r += 1
                else:
                    clist.append(y[i])
                    clist.append("\U0001f44f")

                i += 1
            for k in range(0, len(clist)):
                maste = maste + clist[k]
                k += 1
            return await ctx.send(maste)

    @commands.command(cooldown_after_parsing=True)
    async def ascii(self, ctx, *, text: str):
        art = text2art(text)
        return await ctx.send(f"```{art}```")

    @commands.command(cooldown_after_parsing=True)
    async def randomfont(self, ctx, *, text: str):
        art = text2art(text, "random")
        return await ctx.send(f"```{art}```")

    @commands.command(cooldown_after_parsing=True)
    async def art(self, ctx, type: str = "random"):
        try:
            arto = art(type)
        except artError:
            return await ctx.send(
                "Your chosen art  does not exist/is not supported\n Please check the list of supported arts here: [link](https://pastebin.com/RfsFq1rj)\n Or just use randomart command!"
            )
        else:
            return await ctx.send(arto)

    @commands.command(cooldown_after_parsing=True)
    async def fontify(self, ctx, font: str, *, text: str):
        try:
            arto = text2art(text, font)
        except artError:
            return await ctx.send(
                "Your font does not exist/is not supported\n Please check the list of supported fonts here: [link](https://pastebin.com/P4cu2r0G) or just use the randomfont command!\n Or just use the randomfont command!"
            )
        else:
            return await ctx.send(f"```{arto}```")

    @commands.command(cooldown_after_parsing=True)
    async def randomart(self, ctx):
        y = random.randint(0, 1)
        if y == 0:
            arto = art("rnd-medium")
        else:
            arto = art("random-small")
        return await ctx.send(arto)

    @commands.command(cooldown_after_parsing=True)
    async def monospace(self, ctx, *, text):
        return await ctx.send("`{}`".format(text))

    @commands.command(cooldown_after_parsing=True)
    async def under(self, ctx, *, text):
        return await ctx.send(f"__{text}__")

    @commands.command(cooldown_after_parsing=True)
    async def blue(self, ctx, *, text):
        y = len(text) * "-"
        return await ctx.send(f"```md\n{text}\n{y}```")

    @commands.command(cooldown_after_parsing=True)
    async def orange(self, ctx, *, text):
        return await ctx.send(f"```arm\n{text}```")

    @commands.command(cooldown_after_parsing=True)
    async def yellow(self, ctx, *, text):
        return await ctx.send(f"```http\n{text}```")

    @commands.command(cooldown_after_parsing=True)
    async def green(self, ctx, *, text):
        return await ctx.send(f"```css\n{text}```")

    @commands.command(cooldown_after_parsing=True)
    async def cyan(self, ctx, *, text):
        return await ctx.send(f"```yaml\n{text}```")

    @commands.command(cooldown_after_parsing=True)
    async def red(self, ctx, *, text):
        return await ctx.send(f"```diff\n-{text}```")

    @commands.command(cooldown_after_parsing=True)
    async def spoiler(self, ctx, *, text):
        return await ctx.send("||{}||".format(text))

    @commands.command(cooldown_after_parsing=True)
    async def box(self, ctx, *, text):
        return await ctx.send("```{}```".format(text))

    @commands.command(cooldown_after_parsing=True)
    async def bold(self, ctx, *, text):
        return await ctx.send("**{}**".format(text))

    @commands.command(cooldown_after_parsing=True)
    async def italics(self, ctx, *, text):
        return await ctx.send("*{}*".format(text))

    @commands.command(cooldown_after_parsing=True)
    async def striked(self, ctx, *, text):
        return await ctx.send("~~{}~~".format(text))

    @commands.command(cooldown_after_parsing=True)
    async def emojify(self, ctx, *, text):
        invalidchar = 0
        if len(text) > 1000:
            return await ctx.send("Too long to process")
        else:
            emos = []
            y = str(text)
            capl = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            smalll = "abcdefghijklmnopqrstuvwxyz"
            letst = "0123456789"
            for jool in range(0, len(y)):
                let = y[jool]
                print(let)
                if let == " ":
                    emos.append(2 * "\U00000020")
                elif let == "?":
                    emos.append("\U00002753")
                elif let == "!":
                    emos.append("\U00002757")
                elif let == "":
                    emos.append(2 * "\U00000020")
                elif let in letst:
                    pos = letst.find(let)
                    emos.append("{}\N{combining enclosing keycap}".format(let))
                    emos.append("\U00000020")
                else:
                    pos = capl.find(let)
                    if pos == -1:
                        pos = smalll.find(let)
                        if pos == -1:
                            pos = -1
                            if invalidchar == 0:
                                return await ctx.send(
                                    "invalid characters that are not alphabets, they will be replace by 🇥"
                                )
                                invalidchar += 1
                            else:
                                invalidchar += 1
                    beg = chr(ord("\U0001f1e5") + pos + 1)
                    emos.append(beg)
                    emos.append("\U00000020")
                    jool += 1

            mst = ""
            for i in range(0, len(emos)):
                print(emos[i])
                mst = mst + emos[i]
                i += 1
            return await ctx.send(mst)

    @commands.command(cooldown_after_parsing=True, aliases=["encode"])
    async def encrypt(self, ctx, *, text):
        text = str(text)
        strbytes = text.encode()
        encoded_text = self.cipher_suite.encrypt(strbytes)
        await ctx.author.send(f'Encrypted String\n`{encoded_text}`')

    @commands.command(cooldown_after_parsing=True, aliases=["decode"])
    async def decrypt(self, ctx, *, text):
        text = str(text)
        strbytes = text.encode()
        decoded_text = self.cipher_suite.decrypt(strbytes)
        await ctx.author.send(f"**Finished decryption**\n```{decoded_text}```")

    @commands.command(aliases=['zalgo'])
    async def glitch(self, ctx, *text):
        t = zalgoify.process(text)
        if len(t) > 2000:
            return await ctx.send('Your text is too long!')
        else:
            return await ctx.send(f'{t}')

    @commands.command()
    async def uwu(self, ctx, *, text):
        t = self.uwu.whatsthis(text)
        if len(t) > 2000:
            return await ctx.send('your text is to long')
        else:
            return await ctx.send(t)

    @commands.command()
    async def vapor(self, ctx, *, text):
        t = vaporize(text)
        if len(t) > 2000:
            return await ctx.send('your text is to long')
        else:
            return await ctx.send(t)
