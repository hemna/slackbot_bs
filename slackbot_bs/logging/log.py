import logging
from logging import NullHandler
from logging.handlers import RotatingFileHandler
import queue
import sys

from oslo_config import cfg

from slackbot_bs import conf
from slackbot_bs.logging import rich as slackbot_logging


CONF = cfg.CONF
LOG = logging.getLogger("SLACKBOT_BS")
logging_queue = queue.Queue()


# Setup the logging faciility
# to disable logging to stdout, but still log to file
# use the --quiet option on the cmdln
def setup_logging(loglevel, quiet):
    log_level = conf.log.LOG_LEVELS[loglevel]
    LOG.setLevel(log_level)
    date_format = CONF.logging.date_format
    rh = None
    fh = None

    rich_logging = False
    if CONF.logging.get("rich_logging", False) and not quiet:
        log_format = "%(message)s"
        log_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        rh = slackbot_logging.APRSDRichHandler(
            show_thread=True, thread_width=20,
            rich_tracebacks=True, omit_repeated_times=False,
        )
        rh.setFormatter(log_formatter)
        LOG.addHandler(rh)
        rich_logging = True

    log_file = CONF.logging.logfile
    log_format = CONF.logging.logformat
    log_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    if log_file:
        fh = RotatingFileHandler(log_file, maxBytes=(10248576 * 5), backupCount=4)
        fh.setFormatter(log_formatter)
        LOG.addHandler(fh)

    if not quiet and not rich_logging:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(log_formatter)
        LOG.addHandler(sh)


def setup_logging_no_config(loglevel, quiet):
    log_level = conf.log.LOG_LEVELS[loglevel]
    LOG.setLevel(log_level)
    log_format = CONF.logging.logformat
    date_format = CONF.logging.date_format
    log_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    fh = NullHandler()

    fh.setFormatter(log_formatter)
    LOG.addHandler(fh)

    if not quiet:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(log_formatter)
        LOG.addHandler(sh)
