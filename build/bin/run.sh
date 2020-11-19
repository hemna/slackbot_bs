#!/usr/bin/env bash

export PATH=$PATH:/home/slackbot/.local/bin

telegraf --config /etc/telegraf/telegraf.conf --quiet &

slackbot_bs -c /home/slackbot/conf/slackbot.yaml
