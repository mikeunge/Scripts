#!/usr/bin/env bash
# Cow-spoken fortunes every time you open a terminal
function cowsayfortune {
    NUMOFCOWS=`ls $HOME/.cowsay/cowfiles/ | tail -n +2 | wc -w`
    WHICHCOW=$((RANDOM%$NUMOFCOWS+1))
    THISCOW=`ls $HOME/.cowsay/cowfiles/ | tail -n +2 | sed -e 's/\ /\'$'\n/g' | sed $WHICHCOW'q;d'`

    #echo "Selected cow: ${THISCOW}, from ${WHICHCOW}"
    cowsay -f $THISCOW -W 100
}

cowsayfortune
