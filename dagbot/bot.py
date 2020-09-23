import asyncio
import os
import random
from datetime import datetime

import yaml

import aiohttp
import asyncpg
import discord
import sentry_sdk
from asyncdagpi.client import Client
from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands, menus, tasks
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from utils.badwordcheck import bword
from utils.caching import caching


async def get_prefix(bot, message):
    g_id = message.guild.id
    for e in bot.prefdict:
        if e["server_id"] == str(g_id):
            prefix = e["command_prefix"]
            break

    return commands.when_mentioned_or(prefix)(bot, message)


class Dagbot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description='The number 1 wanna be meme bot',
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(
                roles=False,
                everyone=False)
        )

        with open('./dagbot/data/credentials.yml', 'r') as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)

        self.launch_time = None
        self.session = None
        self.pg_con = None

        self.caching = caching(self)
        self.dagpi = Client(self.data['dagpitoken'])
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
            "developer", "help"
        ]
        for extension in extensions:
            try:
                self.load_extension(f"extensions.{extension}")
                print(f"loaded extension {extension}")
            except Exception as error:
                print(f"{extension} cannot be loaded due to {error}")

        self.before_invoke(self.starttyping)
        # self.after_invoke(self.exittyping)
        self.loop.create_task(self.startdagbot())
        self.socket_stats = {}
        self.sentry = sentry_sdk.init(
            dsn=self.data['sentryurl'],
            integrations=[AioHttpIntegration()],
            release="dagbot@1.2.3"
        )

        self.run(self.data['token'])

    async def process_commands(self, message):
        if message.author.bot and message.guild.id != 491175207122370581:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def startdagbot(self):
        await self.makesession()
        await self.dbconnect()

        self.launch_time = datetime.utcnow()

        await self.caching.prefixcache()
        await asyncio.sleep(1)
        await self.caching.cogcache()
        await asyncio.sleep(1)
        await self.caching.getkeydict()
        await self.get_cog("reddit").memecache()

    async def makesession(self):
        self.session = aiohttp.ClientSession()
        print('made session')

    async def postready(self):
        webhook = Webhook.from_url(
            self.data['onreadyurl'],
            adapter=AsyncWebhookAdapter(
                self.session))
        await webhook.send('Dagbot is Online')

    async def dbconnect(self):
        self.pg_con = await asyncpg.connect(
            host=self.data['dbhost'],
            database=self.data['database'],
            user=self.data['user'],
            password=self.data['dbpassword'],
        )

    async def starttyping(self, ctx):
        await ctx.trigger_typing()

    async def on_command_completion(self, ctx):
        self.commands_called += 1
        try:
            self.useage[ctx.command.qualified_name] += 1
        except KeyError:
            self.useage[ctx.command.qualified_name] = 1

    async def on_ready(self):
        print('Dagbot is ready to roll')
