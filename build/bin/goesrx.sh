#!/usr/bin/env bash

telegraf --config /etc/telegraf/telegraf.conf --quiet &
goesrecv -v -i 1 -c /home/goes/goesrecv.conf
