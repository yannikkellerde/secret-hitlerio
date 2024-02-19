import logging
from termcolor import colored

logger = logging.getLogger("log_util")
logger.setLevel(logging.INFO)
hl = logging.StreamHandler()
hl.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt="%H:%M:%S"))
logger.addHandler(hl)


def log(*messages, level=logging.INFO):
    msg = " ".join(map(str, messages))
    if level == logging.ERROR:
        msg = colored(msg, "red")
    elif level == logging.WARNING:
        msg = colored(msg, "yellow")
    logger.log(level, msg)
