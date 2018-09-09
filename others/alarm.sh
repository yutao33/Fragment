#!/bin/bash
sleep $1
MSG="$1 time over"
notify-send "$MSG" "$MSG"
