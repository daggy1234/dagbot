"""
Copyright ir-3 GNU General Public License v2.0
https://github.com/ir-3/Zane/blob/master/LICENSE
https://github.com/ir-3/Zane/blob/master/zane/logger.py
"""

import logging


class CustomFormatter(logging.Formatter):
    BLACK = "\033[30m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    FORMAT = f"[%(asctime)s - %(name)s - %(levelname)s] {RESET} " \
             f"%(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: BLACK,
        logging.INFO: BLACK,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD + RED
    }

    for k, v in FORMATS.items():
        FORMATS.update({k: v + FORMAT})

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def create_logger(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)

    return logger
