#!/usr/bin/env bash

chmod +x ./text-scaling-factor
sudo cp ./text-scaling-factor /usr/bin/
exit_code=$?
if [ $exit_code -eq 0 ]; then
  echo "Successfully installed text-scaling-factor."
else
  echo "Something went wrong... Please try again. exit_code: $exit_code"
  exit $exit_code 
fi

