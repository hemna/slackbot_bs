import click
import logging
import os
import flask
import pprint
import sys
import yaml

from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError

from slackbot_bs import buzzword as bz
from slackbot_bs import table_flip as tf
from slackbot_bs import constants
import slackbot_bs

LOG = logging.getLogger(__name__)

signing_secret = os.getenv("SLACKBOT_SIGNING_SECRET")
bot_token = os.getenv('SLACK_BOT_TOKEN')

bp = flask.Blueprint('slack_events', __name__)
slack_events_adapter = SlackEventAdapter(signing_secret, "/slack/events", bp)
swc = WebClient(token=bot_token)


def _user_message(user_id: str, channel: str):
    message = "Holy shit you joined!"
    try:
        response = swc.chat_postMessage(message)
    except SlackApiError as e:
        print("message fucked {}".format(e.response['error']))


@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None and "buzzword" in message.get('text'):
        msg = bz.buzzword()
        swc.chat_postMessage(channel=channel, text=msg)


@bp.route('/help', methods=['post'])
def help():
    if flask.request.form['token'] == verification_token:
        msg = constants.HELP_BLOCK
        try:
            channel = flask.request.form['channel_name']
            response = swc.chat_postMessage(channel=channel, blocks=msg)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

        payload = {'text': msg}
        return flask.jsonify(payload)


@bp.route('/wx', methods=['post'])
def weather():
    if flask.request.form['token'] == verification_token:
        msg = "WX: This shit is still being worked on."
        try:
            channel = flask.request.form['channel_name']
            response = swc.chat_postMessage(channel=channel, text=msg)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

        payload = {'text': msg}
        return flask.jsonify(payload)


@bp.route('/buzzword', methods=['POST'])
def buzzword():
    if flask.request.form['token'] == verification_token:
        msg = "{} {}".format(
            flask.request.form['text'],
            bz.buzzword()
        )
        try:
            channel = flask.request.form['channel_name']
            response = swc.chat_postMessage(channel=channel, text=msg)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

        payload = {'text': msg}
        return flask.jsonify(payload)


@bp.route('/tf', methods=['post'])
def table_flip():
    #pprint.pprint(flask.request.form)
    if flask.request.form['token'] == verification_token:
        text = flask.request.form['text']
        user = flask.request.form['user_id']
        try:
            response = swc.users_info(user=user)
            if response.status_code == 200:
                real_name = response.data['user']['real_name']
        except SlackApiError as e:
            # you will get a slackapierror if "ok" is false
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"got an error: {e.response['error']}")
            real_name = flask.request.form["user_name"]


        msg = "{}".format(
            tf.tf(real_name, text)
        )


        try:
            channel = flask.request.form['channel_name']
            response = swc.chat_postMessage(channel=channel, text=msg)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

        payload = {'text': msg}
        return flask.jsonify(payload)


@slack_events_adapter.on("team_join")
def join(payload):

    event = payload.get("event", {})
    user_id = event.get("user", {}).get("id")

    try:
        response = swc.im_open(user_id)
        channel = response["channel"]["id"]

    except SlackApiError as e:
        print("join fucked {}".format(e.response['error']))



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



def join_channels(slackbot_config):
    channels = slackbot_config['channels']
    try:
        channel_list = swc.conversations_list()
        #LOG.debug(channel_list)
        for channel in channels:
            channel_id = None
            for info in channel_list['channels']:
                if info['name'] == channel:
                    channel_id = info['id']

            if not channel_id:
                LOG.error("Can't find channel {}".format(channel))
            else:
                #info = swc.conversations_info(channel=channel_id)
                swc.conversations_join(channel=channel_id)
                #msg = "I'm back online bitches!"
                #response = swc.chat_postMessage(channel=channel_id,
                #                                text=msg)

    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


@click.command()
@click.option("--port", metavar="<port>", default=9102,
              help="specify exporter serving port")
@click.option("-c", "--config", metavar="<config>",
              help="path to rest config")
def main(port, config):
    """Console script for slackbot_bs."""
    global verification_token

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
    verification_token = slackbot_config['slack']['verification_token']

    join_channels(slackbot_config)

    app = flask.Flask(__name__)

    app.register_blueprint(bp)
    app.run(port=6000, host='0.0.0.0')

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
