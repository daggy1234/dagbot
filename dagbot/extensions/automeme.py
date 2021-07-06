import asyncio

from dagbot.bot import Dagbot

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
                embed = await self.bot.reddit_cog.meme_embed()
                await webhook.send("Automeme", embed=embed)
        self.bot.logger.debug("AUTOMEMES DISPATCHED")

    @automeme_post.before_loop
    async def before_autoemer(self):
        self.bot.logger.info("Waiting for automemer")
        await self.bot.wait_until_ready()
        await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(automeme(bot))
