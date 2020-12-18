from discord.ext import commands
from discord.ext.commands import context

class MyContext(commands.Context):

    async def send(self, content=None, *, tts=False, embed=None, file=None,
                                          files=None, delete_after=None, nonce=None,
                                          allowed_mentions=None):
        bot = self.bot

        if content:
            for key,val in bot.data.items():
                content = content.replace(val,f"[ Omitted {key} ]")
        else:
            content = ""
        if len(content) > 2000:
            if embed:
                await super().send("Little long there woul you like me to upload this?")
        else:
            return await super().send(content,file=file,embed=embed,files=files, delete_after=delete_after, nonce=nonce,
                                          allowed_mentions=allowed_mentions, tts=tts)

    async def safe_send(self, yes):
        print("yes")
    