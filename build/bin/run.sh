#!/usr/bin/env bash

export PATH=$PATH:/home/slackbot/.local/bin

telegraf --config /etc/telegraf/telegraf.conf --quiet &

export SLACK_BOT_TOKEN="xoxb-1493666375863-1508131809445-3ciwSob1TLm8r8ZscMmN8MZp"
export SLACKBOT_SIGNING_SECRET="c74a70c29924ab8e8aa44582fd1b908b"

slackbot_bs -c /home/slackbot/conf/slackbot.yaml
