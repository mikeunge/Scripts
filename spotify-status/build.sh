#!/usr/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "Please run as root"
	exit
fi

if ! [ -f "./spotifystatus.sh" ]; then
	echo "Spotifystatus was not found"
	exit
fi

# remove the .sh when copying
sudo cp ./spotifystatus.sh /usr/bin/spotifystatus
