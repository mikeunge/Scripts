#!/usr/bin/env bash
#
# install.sh - Install the tt_daemon and tt.
#

cd ./daemon/
go build -o tt_daemon
if [ $? -eq 0 ]; then
  echo "Successfully built the tt daemon."
else
  echo "Something went wrong... Please try again. exit_code: $?"
  exit 1
fi
cd ..

sudo cp ./daemon/tt_daemon /usr/bin/
if [ $? -eq 0 ]; then
  echo "Successfully installed the tt daemon."
else
  echo "Something went wrong... Please try again. exit_code: $?"
  exit 1 
fi

sudo cp ./tt /usr/bin/
if [ $? -eq 0 ]; then
  echo "Successfully installed tt, please try running 'tt --help' to see if it works."
else
  echo "Something went wrong... Please try again. exit_code: $?"
  exit 1
fi
