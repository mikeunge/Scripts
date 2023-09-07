#!/usr/bin/env bash

sudo cp ./screenshot /usr/bin/
exit_code=$?
if [ $exit_code -eq 0 ]; then
  echo "Successfully installed screenshot."
else
  echo "Something went wrong... Please try again. exit_code: $exit_code"
  exit $exit_code 
fi

