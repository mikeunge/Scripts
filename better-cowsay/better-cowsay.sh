#!/usr/bin/env bash

# @todo: add a cli param to load a specific cow-file

function bettercowsay {
    NUMOFCOWS=`ls $HOME/.cowsay/cowfiles/ | tail -n +2 | wc -w`
    WHICHCOW=$((RANDOM%$NUMOFCOWS+1))
    THISCOW=`ls $HOME/.cowsay/cowfiles/ | tail -n +2 | sed -e 's/\ /\'$'\n/g' | sed $WHICHCOW'q;d'`
    cowsay -f $THISCOW -W 100
}

bettercowsay
