import os

from .bot import Dagbot
import logging
import logging.handlers


if __name__ == "__main__":
    os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
    os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
    os.environ["JISHAKU_HIDE"] = "True"
    root_logger = logging.getLogger()
    root_logger.addHandler(logging.handlers.SysLogHandler())
    dagbot = Dagbot()
    dagbot.run(dagbot.data['token'])
