from functools import update_wrapper
import logging
from pathlib import Path
import typing as t

import click
from oslo_config import cfg

from slackbot_bs import conf  # noqa: F401
from slackbot_bs.logging import log


CONF = cfg.CONF
home = str(Path.home())
DEFAULT_CONFIG_DIR = f"{home}/.config/slackbot_bs/"
DEFAULT_CONFIG_FILE = f"{home}/.config/slackbot_bs/slackbot_bs.conf"


F = t.TypeVar("F", bound=t.Callable[..., t.Any])

common_options = [
    click.option(
        "--loglevel",
        default="INFO",
        show_default=True,
        type=click.Choice(
            ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
            case_sensitive=False,
        ),
        show_choices=True,
        help="The log level to use for log",
    ),
    click.option(
        "-c",
        "--config",
        "config_file",
        show_default=True,
        default=DEFAULT_CONFIG_FILE,
        help="The config file to use for options.",
    ),
    click.option(
        "--quiet",
        is_flag=True,
        default=False,
        help="Don't log to stdout",
    ),
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


def process_standard_options(f: F) -> F:
    def new_func(*args, **kwargs):
        ctx = args[0]
        ctx.ensure_object(dict)
        config_file_found = True
        if kwargs["config_file"]:
            default_config_files = [kwargs["config_file"]]
        else:
            default_config_files = None
        try:
            CONF(
                [], project="slackbot_bs", version="1.0",
                default_config_files=default_config_files,
            )
        except cfg.ConfigFilesNotFoundError:
            config_file_found = False
        except cfg.RequiredOptError as ex:
            print(ex)
            exit(-1)
        ctx.obj["loglevel"] = kwargs["loglevel"]
        # ctx.obj["config_file"] = kwargs["config_file"]
        ctx.obj["quiet"] = kwargs["quiet"]
        log.setup_logging(
            ctx.obj["loglevel"],
            ctx.obj["quiet"],
        )
        #if CONF.trace_enabled:
        #    trace.setup_tracing(["method", "api"])

        if not config_file_found:
            LOG = logging.getLogger("SLACKBOT_BS")   # noqa: N806
            LOG.error("No config file found!!")

        del kwargs["loglevel"]
        del kwargs["config_file"]
        del kwargs["quiet"]
        return f(*args, **kwargs)

    return update_wrapper(t.cast(F, new_func), f)


def process_standard_options_no_config(f: F) -> F:
    """Use this as a decorator when config isn't needed."""
    def new_func(*args, **kwargs):
        ctx = args[0]
        ctx.ensure_object(dict)
        ctx.obj["loglevel"] = kwargs["loglevel"]
        ctx.obj["config_file"] = kwargs["config_file"]
        ctx.obj["quiet"] = kwargs["quiet"]
        log.setup_logging_no_config(
            ctx.obj["loglevel"],
            ctx.obj["quiet"],
        )

        del kwargs["loglevel"]
        del kwargs["config_file"]
        del kwargs["quiet"]
        return f(*args, **kwargs)

    return update_wrapper(t.cast(F, new_func), f)
