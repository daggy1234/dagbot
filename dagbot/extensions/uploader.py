import asyncio
import aiohttp

from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands, tasks


class Uploader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stat_post.start()

    @tasks.loop(minutes=30)
    async def stat_post(self):
        url = "https://dagbot-site.herokuapp.com/api/newstats"
        stats = {
            "servers": len(self.bot.guilds),
            "users": sum([g.member_count for g in self.bot.guilds]),
            "commands_called": self.bot.commands_called,
            "socket_stats": [self.bot.socket_stats],
            "command_stats": [self.bot.useage]
        }
        headers = {"Token": self.bot.data["stats"]}
        r = await self.bot.session.post(url, data=stats, headers=headers)
        if r.status != 200:
            self.bot.logger.critical("STAT POST ERROR")
            raise aiohttp.ClientError("Fuck no 200 for API")
        else:
            self.bot.logger.debug("Stats posted")

    @stat_post.before_loop
    async def before_post(self):
        self.bot.logger.info("Waiting for Ready")
        await self.bot.wait_until_ready()
        await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(Uploader(bot))
