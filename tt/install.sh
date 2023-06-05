#!/usr/bin/env bash
#
# install.sh - Install the tt_daemon and tt.
#

sudo cp ./daemon /usr/bin/tt_daemon
if [ $? -eq 0 ]; then
  echo "Successfully installed the tt daemon."
else
  echo "Something went wrong... Please try again. exit_code: $?"
fi

sudo cp ./tt /usr/bin/
if [ $? -eq 0 ]; then
  echo "Successfully installed tt, please try running 'tt --help' to see if it works."
else
  echo "Something went wrong... Please try again. exit_code: $?"
fi
