import asyncio
from typing import Optional

from dagbot.bot import Dagbot
from dagbot.extensions.reddit import reddit

from discord import Webhook
from discord.ext import commands, tasks


class automeme(commands.Cog):
    def __init__(self, bot):
        self.bot: Dagbot = bot
        self.automeme_post.start()

    @tasks.loop(minutes=5)
    async def automeme_post(self):
        for record in self.bot.automeme_data:
            if record["active"]:
                webhook = Webhook.from_url(record["webhook_url"],session=self.bot.session)
                cog: Optional[reddit] = self.bot.get_cog("reddit")
                if not cog:
                    continue
                embed = await cog.meme_embed()
                await webhook.send("Automeme", embed=embed)
        self.bot.logger.debug("AUTOMEMES DISPATCHED")

    @automeme_post.before_loop
    async def before_autoemer(self):
        self.bot.logger.info("Waiting for automemer")
        await self.bot.wait_until_ready()
        await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(automeme(bot))
