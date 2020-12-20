import asyncio
import logging
from datetime import datetime

import aiohttp
import asyncpg
import discord
import sentry_sdk
import yaml
from asyncdagpi import Client
from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from .utils.badwordcheck import bword
from .utils.caching import caching
from .utils.logger import create_logger
from .utils.context import MyContext


async def get_prefix(bot, message):
    g_id = message.guild.id
    for e in bot.prefdict:
       if e["server_id"] == str(g_id):
           prefix = e["command_prefix"]
           break
    return commands.when_mentioned_or(prefix)(bot, message)


def make_intents() -> discord.Intents:
    intents = discord.Intents.none()
    intents.guilds = True
    intents.messages = True
    intents.reactions = True
    return intents


class Dagbot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description='The number 1 wanna be meme bot',
            case_insensitive=True,
            max_messages=100,
            allowed_mentions=discord.AllowedMentions(
                roles=False,
                everyone=False),
            intents=make_intents()
        )

        self.logger = create_logger("Dagbot", logging.DEBUG)
        with open('./configuration.yml', 'r') as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        self.data.pop("PWD")
        self.logger.info("Loaded Config File")
        self.launch_time = None
        self.session = None
        self.pool = None
        self.dagpi = None
        self.caching = caching(self)
        self.bwordchecker = bword()
        self.bwordchecker.loadbword()
        self.useage = {}
        self.commands_called = 0

        # self.add_cog(Help(bot))

        self.load_extension("jishaku")

        extensions = [
            "text", "fun", "newimag",
            "reddit", "games", "util",
            "whysomart", "animals", "memes",
            "tags", "misc", "settings",
            "ai", "events", "errors",
            "developer", "help", "automeme", "uploader"
        ]
        for extension in extensions:
            try:
                self.load_extension(f"dagbot.extensions.{extension}")
                self.logger.info(f"loaded extension {extension}")
            except Exception as error:
                self.logger.critical(
                    f"{extension} cannot be loaded due to {error}")

        self.before_invoke(self.starttyping)
        self.logger.info("Initialising Stuff")
        self.loop.create_task(self.startdagbot())
        self.socket_stats = {}
        self.sentry = sentry_sdk.init(
            dsn=self.data['sentryurl'],
            integrations=[AioHttpIntegration()],
            release="dagbot@2.0.0"
        )
        self.logger.info("Ready to roll")

    async def process_commands(self, message):
        if message.author.bot and message.guild.id != 491175207122370581:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def get_context(self, message, *, cls=MyContext):
        # when you override this method, you pass your new Context
        # subclass to the super() method, which tells the bot to
        # use the new MyContext class
        return await super().get_context(message, cls=cls)

    async def startdagbot(self):
        await self.makesession()
        await self.dbconnect()

        self.launch_time = datetime.utcnow()
        self.logger.info("Started DAGBOT")
        await self.caching.prefixcache()
        await asyncio.sleep(1)
        await self.caching.cogcache()
        await asyncio.sleep(1)
        await self.caching.getkeydict()
        await self.caching.automemecache()
        await self.get_cog("reddit").memecache()

    async def makesession(self):
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.logger.info('made session')
        self.dagpi = Client(self.data['dagpitoken'],
                            loop=self.loop,
                            session=self.session)
        self.logger.info("Dagpi Initialised")

    async def postready(self):
        webhook = Webhook.from_url(
            self.data['onreadyurl'],
            adapter=AsyncWebhookAdapter(
                self.session))
        await webhook.send('Dagbot is Online')

    async def dbconnect(self):
        try:
            self.pool = await asyncpg.create_pool(
                host=self.data['dbhost'],
                database=self.data['database'],
                user=self.data['user'],
                password=self.data['dbpassword'],
            )
            self.logger.info("Connected to the Database")
        except Exception:
            self.logger.critical("DB COULDN'T CONNECT")

    async def starttyping(self, ctx):
        await ctx.trigger_typing()

    async def on_command_completion(self, ctx):
        self.commands_called += 1
        try:
            self.useage[ctx.command.qualified_name] += 1
        except KeyError:
            self.useage[ctx.command.qualified_name] = 1

    async def on_ready(self):
        self.logger.info('Dagbot is ready to roll')
