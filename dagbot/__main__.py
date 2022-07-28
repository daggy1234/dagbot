import os

from .bot import Dagbot
import asyncio


async def start_bot():
    dagbot: Dagbot = Dagbot()
    await dagbot.startdagbot()
    try:
        await dagbot.start(dagbot.data['token'])
    except KeyboardInterrupt:
        await dagbot.close()


if __name__ == "__main__":
    os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
    os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
    os.environ["JISHAKU_HIDE"] = "True"
    asyncio.run(start_bot())
    
    
