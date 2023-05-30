#!/usr/bin/env bash

# get the spotify status (playing, paused)
status=$(playerctl -p spotify status)
if [ $? -ne 0 ]; then
	exit 1
fi
if [ $status == "Playing" ]; then
	echo ""
elif [ $status == "Paused" ]; then
	echo ""
else
	# Shouldn't happen but yeah ;)
	echo ""
fi
