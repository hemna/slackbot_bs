import click
import logging
import os
import sys
from typing import Callable

from dotenv import load_dotenv
from oslo_config import cfg
from slack_bolt import App, Ack, Respond, Say, BoltContext
from slack_sdk.models.blocks import (
    SectionBlock,
    MarkdownTextObject
)

from aprsd.rpc import client as rpc_client

from slackbot_bs.slackbot_bs import cli
from slackbot_bs import cli_helper


LOG = logging.getLogger("SLACKBOT_BS")
CONF = cfg.CONF

env_path = ".env"
load_dotenv(env_path)

signing_secret = os.getenv("SLACK_SIGNING_SECRET")
if not signing_secret:
    click.echo("No SLACK_SIGNING_SECRET env var set")
    sys.exit(-1)
bot_token = os.getenv('SLACK_BOT_TOKEN')
if not bot_token:
    click.echo("No SLACK_BOT_TOKEN env var set")
    sys.exit(-1)

# Create the slack app
app = App(token=os.environ['SLACK_BOT_TOKEN'],
          signing_secret=os.environ["SLACK_SIGNING_SECRET"])

@app.middleware
def log_request(logger: logging.Logger, body: dict, next: Callable):
    logger.debug(body)
    return next()


@app.event("app_mention")
def event_test(body: dict, say, logger: logging.Logger):
    LOG.debug(body)
    say(f"What's up? <@{body['event']['user']}>")



@app.command('/aprsd-test')
def aprsd_test(body: dict, ack: Ack, respond: Respond, command):
    ack(
        text="Accepted Request",
        blocks=[
            SectionBlock(
                block_id="b",
                text=MarkdownTextObject(text=":white_check_mark: Accepted. Calling APRSD to fetch stats!"),
            )
        ],
    )
    LOG.debug(f"/aprsd-test CALLED ")
    cl = rpc_client.RPCClient()
    stats = cl.get_stats_dict()
    count = 0
    for entry in stats['aprsd']['seen_list']:
        count += 1

    del stats['aprsd']['seen_list']
    LOG.debug(stats)

    respond(
        text="aprsd version",
        blocks=[
            SectionBlock(
                block_id="aprsd",
                text=MarkdownTextObject(text=(
                    f"REPEAT Service Running APRSD: {stats['aprsd']['version']} "
                    )
                )
            ),
            SectionBlock(
                block_id="Uptime",
                text=MarkdownTextObject(text=f"Uptime: {stats['aprsd']['uptime']}"),
            ),
            SectionBlock(
                block_id="aprsd_connected",
                text=MarkdownTextObject(text=f"Connected to APRS-IS Server: {stats['aprs-is']['server']}"),
            ),
            SectionBlock(
                block_id="aprsd_packets",
                text=MarkdownTextObject(
                    text=(
                        f"Packets: RX:{stats['packets']['received']}    "
                        f"TX:{stats['packets']['sent']} "
                    ),
                ),
            ),
            SectionBlock(
                block_id="aprsd_messages",
                text=MarkdownTextObject(
                    text=(
                        f"Messages: RX:{stats['messages']['received']}    "
                        f"TX:{stats['messages']['sent']} "
                    ),
                ),
            ),
            SectionBlock(
                block_id="aprsd_seen",
                text=MarkdownTextObject(
                    text=(
                        f"Unique callsigns have used REPEAT {count}"
                    ),
                ),
            ),
        ],
    )


@app.error
def global_error_handler(error, body, logger):
    logger.exception(error)
    logger.debug(body)


@cli.command()
@cli_helper.add_options(cli_helper.common_options)
@click.pass_context
@cli_helper.process_standard_options
def bot(ctx):
    """Run the bot."""
    # Dump all the config options now.
    CONF.log_opt_values(LOG, logging.DEBUG)
    app.start(port=CONF.slack_web_port)

