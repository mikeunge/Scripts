#!/bin/bash
#
# backupper.sh
# version: 1.0.2.4
#
# Author:	Ungerböck Michele
# Github:	github.com/mikeunge
# Company:	GEDV GmbH
#
# All rights reserved.
#
# Get start time and date_only.
start_date=`date +”%d-%m-%Y”`
script_start=`date +"%Y-%m-%d %T"`

# Load the config.
CONFIG_FILE="/etc/backupper.conf"   # change this path if needed.
if [ -f "$CONFIG_FILE" ]; then
    source $CONFIG_FILE
else
    echo "Configuration file doesn't exist! [$CONFIG_FILE]"
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

    # Get the current datetime.
    cur_datetime=`date +"%Y-%m-%d %T"`
    # Write the message to the log file.
    echo "[$cur_datetime] ${priority} : ${message}" >> $LOG_FILE
}

send_email() {
    log "Sending email..." "DEBUG"
    mutt -s "$SENDER [$status] (exec=$JOB) - $start_date" -a $RSNAPSHOT_LOG_FILE -- $DEST_EMAIL < $LOG_FILE
}

panic() {
    # Check if a argument is provided.
    if [ -z "$1" ]; then
        error=1
    else
        error="$1"
    fi
    # Check if error is true (0).
    if (( $error == 0 )); then
       status="error"
       log "Something went wrong while creating the backup. Please check the logfile in the attachment." "ERROR"
       send_email
       exit 1
    else
       status="success"
       log "Backup was successfully created!" "INFO"
       send_email
       exit 0
    fi
}

# Check if the log_rotate is set.
# If so, remove the defined logs for cleaner output.
if [[ $LOG_ROTATE == 1 ]]; then
    log "LOG_ROTATE is active.." "DEBUG"
    # Check if the logfiles exist, if so, delete them.
    log_files=( "$RSNAPSHOT_LOG_FILE" "$LOG_FILE" )
    for file in "${log_files[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
            log "Deleted logfile $file" "DEBUG"
        else
            log "$file doesn't exist.." "DEBUG"
        fi
    done
fi

log "*.backupper.sh start.*" "INFO"

# Check if a argument is provided.
if [ -z "$1" ]; then
    log "No argument supplied, fallback to config defined job => $DEFAULT_JOB"
    JOB="$DEFAULT_JOB"
else
    JOB="$1"
    log "Job to execute => $JOB" "DEBUG"
fi

# Check if the second job is executed.
if [[ "$SEC_JOB" == "$JOB" ]]; then
    SHARE="$SEC_SHARE"
fi

# Unmount a drive (if mounted) to assure the mounting is going to be successfull.
umount "$MOUNT"

# Try to mount the network drive.
i=0
while [[ $i < $TRIES ]]; do
    # TODO: Check if the mounting point exists!
    if ! grep -q "$MOUNT" /proc/mounts; then
        { # Try and mount the network drive.
            log "Mounting share ... [$SHARE]" "INFO"
            mount -t cifs -o username="$USER",password="$PASSWORD" "$SHARE" "$MOUNT" > /dev/null 2>&1
            log "Network drive successfully mounted!" "INFO"
            break
        } || {
            (( i=i+1 ))
            log "[$i/$TRIES] Could not mount the network drive! ... [$SHARE -> $MOUNT]" "WARNING"
            if [[ i == $TRIES ]]; then
                log "Could not mount the network drive $TRIES times!\nExiting script!" "ERROR"
                panic 1
            fi
        }
    else	# If the drive is already mounted.
        log "Network drive is already mounted!" "DEBUG"
        break
    fi
done

log "Starting backup job ... [$JOB]" "INFO"
{
    # Run the rsnapshot backup job.
    cmd="$RSNAPSHOT $JOB"
    output=`$cmd`
    # Check if the rsnapshot output is empty or not.
    if [[ $output != "" ]]; then
        log "$output" "INFO"
    else
        log "rSnapshot didn't return any output.." "WARNING"
    fi
} || {
    # Built a wrapper around a rsnapshot error that happens if a file changes while rsnapshot runs (return_val: 2).
    if [ $output -eq 0 ] -eq 2 ]; then
        log "Backup complete." "INFO"
        script_end=`date +"%Y-%m-%d %T"`
    else
        log "Something went wrong with the backup... Please check the rSnapshot logs.." "ERROR"
        panic 1
    fi
}

log "Start: $script_start :: End: $script_end" "INFO"
panic 0