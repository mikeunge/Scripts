#!/usr/bin/env bash

chmod +x ./scale
sudo cp ./scale /usr/bin/
exit_code=$?
if [ $exit_code -eq 0 ]; then
  echo "Successfully installed text-scaling-factor."
  echo "You can now use it as 'scale up|down'"
else
  echo "Something went wrong... Please try again. exit_code: $exit_code"
  exit $exit_code 
fi

