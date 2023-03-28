import click
import logging
import os
import flask
import pprint
import sys
import yaml

from dotenv import load_dotenv
from slack_bolt import App

from slackbot_bs import buzzword as bz
from slackbot_bs import table_flip as tf
from slackbot_bs import constants
import slackbot_bs

LOG = logging.getLogger(__name__)

env_path = ".env"
load_dotenv(env_path)

print(f"SLACK_BOT_TOKEN {os.environ['SLACK_BOT_TOKEN']}")
print(f"SLACK_SIGNING_SECRET {os.environ['SLACK_SIGNING_SECRET']}")

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

@app.command('/help')
def help(ack, body):
    LOG.info(body)
    ack("Holy shit help!")


@app.event("app_mention")
def event_test(body, say, logger):
    LOG.info(body)
    say("What's up?")


@app.command('/wx')
def weather(ack, body, respond):
    LOG.info(body)
    msg = "WX: This shit is still being worked on."
    respond(msg)


@app.command('/buzzword')
def buzzword(ack, body, respond):
    LOG.info(body)
    msg = "{} {}".format(
        flask.request.form['text'],
        bz.buzzword()
    )
    respond(msg)


def get_config(config_file):
    if os.path.exists(config_file):
        try:
            with open(config_file) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        except IOError as e:
            logging.error("Couldn't open configuration file: " + str(e))
        return config
    else:
        logging.error("Config file doesn't exist: " + config_file)
        exit(0)

@app.error
def global_error_handler(error, body, logger):
    logger.exception(error)
    logger.info(body)


@click.command()
@click.option("--port", metavar="<port>", default=3000,
              help="specify exporter serving port")
@click.option("-c", "--config", metavar="<config>",
              help="path to rest config")
def main(port, config):
    """Console script for slackbot_bs."""
    global app

    config_obj = get_config(config)
    slackbot_config = config_obj['slackbot']

    if slackbot_config['log_level']:
        LOG.setLevel(logging.getLevelName(
            slackbot_config['log_level'].upper()))
    else:
        LOG.setLevel(logging.getLevelName("INFO"))

    format = '[%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(stream=sys.stdout, format=format)

    LOG.info("Starting SlackBot Bullshitter {} on port={} config={}".format(
        slackbot_bs.version_string(),
        port,
        config
    ))

    app.start(port)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
