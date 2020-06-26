#!/bin/bash
#
# backup.sh
# version: 1.0.2
#
# Author:	Ungerböck Michele
# Github:	github.com/mikeunge
# Company:	GEDV GmbH
#
# All rights reserved.
#
# Load the config.
CONFIG_FILE="./backup.conf"
if [ -f "$CONFIG_FILE" ]; then
    source $CONFIG_FILE
else 
    exit 1
fi

# Define the log levels and the log level that is used.
declare -A levels=([DEBUG]=0 [INFO]=1 [WARNING]=2 [ERROR]=3)

log() {
	# Bind the passed parameters.
    local message=$1
    local priority=$2

	# Check if level exists.
    [[ ${levels[$priority]} ]] || return 1

    # Check if level is enough.
    (( ${levels[$priority]} < ${levels[$LOG_LEVEL]} )) && return 2
	{
		# Write the message to the log file.
    	echo "${priority} : ${message}" >> $LOG_FILE
	} || {
		# Could not create log.. Remember error and when script is done, panic.
		script_failure=true
	}
}


send_email() {
	# Run the mailman.py script to send emails.
	# Requires python3 installed on the machine!
	mail -s "Test Subject" user@example.com < /dev/null
}


panic() {
    # Exits the script and outputs a message if given.
    error=$1
    msg=$2
    # Check if a message is given, if so, echo it out.
    if [ ! -z "$msg" ]; then
        log $msg
    fi
    # Check if error is true (0).
    if (( $error == 0 )); then
        exit 1
    else
        exit 0
    fi
}


# Try to mount the network drive.
i=0
while [ i < $TRIES ]; do
	if ! [[ grep -qs $MOUNT /proc/mounts ]]; then
		{ # Try and mount the network drive.
			log "mounting share ... [$SHARE]" "INFO"
			mount -t cifs -o username=$USER,password=$PASSWORD $SHARE $MOUNT > /dev/null 2>&1
			break
		} || {
			(( i=i+1))
			log "[$i/$TRIES] Could not mount the network drive! ... [$SHARE -> $MOUNT]" "ERROR"
			if [[ i == $TRIES ]]; then
				panic 1 "Could not mount the network drive $TRIES times!\nExiting script!"
			fi
		}
	else	# If the drive is already mounted.
		break
	fi
done
log "Drive is mounted!" "INFO"


log "Starting backup job ... [$JOB]" "INFO"
{ 
	# Run the rsnapshot backup job.
	cmd="/usr/bin/rsnapshot $JOB"
	output=$(eval $cmd)
	log $output "INFO"
} || {
	log "Something went wrong with the backup... Please check the rsnapshot logs.." "ERROR"
	panic 1 "Could not run the rsnapshot backup job! Please check the logs for more information.."
}

if [[ script_failure == true ]]; then
	log "Script is finished, errors occured. Please check the logfile for more information." "ERROR"
fi

send_email
log "Done." "INFO"
panic 0
