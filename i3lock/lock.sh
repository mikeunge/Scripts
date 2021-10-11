#!/bin/bash
icon=$HOME/Pictures/Icon/md_todo_round.png
tmp=/tmp/screen.png
scrot /tmp/screen.png
convert $tmp -scale 10% -scale 1000% $tmp
convert $tmp $icon -gravity center -composite -matte $tmp
# stop music
# dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop
i3lock -u -i $tmp
rm $tmp
