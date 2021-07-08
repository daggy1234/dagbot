from __future__ import annotations
from typing import Union, Optional, TYPE_CHECKING
import discord
from discord.ext import commands
if TYPE_CHECKING:
    from dagbot.bot import Dagbot


class Confirm(discord.ui.View):

    def __init__(self, ctx: MyContext, user: discord.User):
        super().__init__(timeout=100.0)
        self.value: bool = False
        self.ctx = ctx
        self.user = user


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        assert interaction.user is not  None
        check = self.user.id == interaction.user.id
        if check:
            return True
        else:
            await interaction.response.send_message("Not your help menu :(", ephemeral=True)
            return False



    async def on_timeout(self) -> None:
        await self.ctx.send(f"{self.ctx.author.mention} No option selected within 100s")
        return await super().on_timeout()


    @discord.ui.button(label='✓', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Confirmed!', ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='x', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Cancelled', ephemeral=True)
        self.value = False
        self.stop()


class MyContext(commands.Context):

    bot: Dagbot
    guild: discord.Guild
    author: discord.Member
    message: discord.Message
    channel: Union[discord.TextChannel, discord.Thread, discord.DMChannel, discord.GroupChannel]

    async def send(self,         
        content: Optional[str] = None,
        *,
        tts: bool = None,
        embed: discord.Embed = None,
        file: discord.File = None,
        delete_after: float = None,
        nonce: Union[str, int] = None,
        allowed_mentions: discord.AllowedMentions = None,
        reference: Union[discord.Message, discord.MessageReference] = None,
        mention_author: bool = None,
        view: discord.ui.View = None,
):
        bot = self.bot

        if content:
            for key, val in bot.data.items():
                if key not in ["imgflipuser", "database"]:
                    content = content.replace(val, f"[ Omitted {key} ]")
        else:
            content = ""
        if embed:
            desc = embed.description
            if desc:
                for key, val in bot.data.items():
                    if key not in ["imgflipuser", "database"]:
                        desc = desc.replace(val, f"[ Ommited {key}]")
                embed.description = desc
            embed.color = self.guild.me.color
            if len(embed) > 2048:
                return await super().send("This embed is a little too large "
                                          "to send.")
        if len(content) > 2000:
            return await super().send("Little long there woul you like me to "
                                      "upload this?")

        #typeignore
        return await super().send(content, file=file, embed=embed, 
                                  delete_after=delete_after, nonce=nonce,
                                  allowed_mentions=allowed_mentions, tts=tts, view=view) # type: ignore

    async def safe_send(self, yes):
        await super().send("Yes this method is cool")

    async def confirm(self, propmpt: str, *, user: Optional[discord.User] = None) -> bool:
        embed = discord.Embed(title="Requesting Confirmation", description=propmpt, color=self.guild.me.color)
        embed.set_author(name=self.author.name, icon_url=self.author.avatar.url)
        user_conf = user or self.author._user
        view = Confirm(self, user_conf)
        await self.send(embed=embed, view=view)
        await view.wait()
        return view.value


