#!/usr/bin/env bash
#
# Notifier.sh
# Version 1.0.0
# Author: @mikeunge
# 
# Run notify.sh with a parameter you want to hook on.
# The script runs a "ps aux" and greps the output for the given parameter, when the process finishes you get a notification via e-mail.
#
#############################
# Define global vars below. #
#############################
locked=1        # lock process
sleep_time=5    # define seconds

panic() {
    # Exits the script and outputs a message if given.
    error=$1
    msg=$2
    # Check if a message is given, if so, echo it out.
    if [ ! -z "$msg" ]; then
        echo $msg
    fi
    # Check if error is true (0).
    if (( $error == 0 )); then
        exit 1
    else
        exit 0
    fi
}

check_process() {
    # Get all processes, grep them, remove the grep and the script for accuracy.
    cmd="ps aux | grep '$1' | grep -v grep | grep -v notify.sh"
    out=$(eval $cmd)
    if [ -z "$out" ]; then
        return 1
    else
        return 0
    fi
}

init() {
    # Initialize the script.
    # Make sure the prcess to monitor is running.
    check_process $param
    if (( $? == 0 )); then
        # Lock the process.
        locked=0
    else
        panic 1 "[$param] does not exist.. Exiting.."
    fi
}

# Check if a parameter is provided.
if [ -z "$1" ]; then
    panic 1 "No parameters are given.. Exiting."
else
    param=$1
fi

init
# As long the process is hooked, it get's checked frequently.
while (( $locked == 0 )); do
    check_process $param
    if (( $? == 0 )); then
        echo "[$param] is running.."
        sleep $sleep_time
    else 
        locked=1
    fi
done

# Send e-mail and exit the script.
panic 0 "[$param] isn't running anymore. Exiting."