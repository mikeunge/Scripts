#!/bin/bash
#
# backupper.sh
# version: 1.0.2.7
#
# Author:	Ungerböck Michele
# Github:	github.com/mikeunge
# Company:	GEDV GmbH
#
# All rights reserved.
#
# Get start time and date_only.
start_date=$(date +'%d.%m.%Y')
script_start=$(date +'%d.%m.%Y %T')

# Load the config.
CONFIG_FILE="/etc/backupper.conf"   # change this path if needed.
if [ -f "$CONFIG_FILE" ]; then
    source $CONFIG_FILE
else
    # If config is not found, log to a specific .error.log file.
    echo "Configuration file doesn't exist! [$CONFIG_FILE]" > /var/log/backupper.error.log
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
    cur_datetime=$(date +'%d.%m.%Y %T')
    # Write the message to the log file.
    echo "${priority} : [$cur_datetime] : ${message}" >> $LOG_FILE
}

send_email() {
    log "Sending email via $MAIL_CLIENT..." "DEBUG"
    # Check if the mail_client is defined correctly.
    if $MAIL_CLIENT == "sendmail"; then
        mail -A $RSNAPSHOT_LOG_FILE -s "$SENDER [$status] (exec=$JOB) - $start_date" $DEST_EMAIL < $LOG_FILE
    elif $MAIL_CLIENT == "mail"; then
        mail -A $RSNAPSHOT_LOG_FILE -s "$SENDER [$status] (exec=$JOB) - $start_date" $DEST_EMAIL < $LOG_FILE
    elif $MAIL_CLIENT == "mutt"; then
        mutt -s "$SENDER [$status] (exec=$JOB) - $start_date" -a $RSNAPSHOT_LOG_FILE -- $DEST_EMAIL < $LOG_FILE
    else
        log "Could not send the e-mail; Mail client ($MAIL_CLIENT) is not/or wrong defined. Please check the config. ($CONFIG_FILE)" "ERROR"
        panic 1
    fi
}

panic() {
    # Check if a argument is provided.
    if [ -z "$1" ]; then
        error=1
    else
        error=$1
    fi
    # Check if error is true (0).
    if (( $error == 0 )); then
       status="error"
       log "An error occured, please check the mail content and/or the attachment for more informations." "ERROR"
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
    log "LOG_ROTATE is active." "DEBUG"
    # Check if the logfiles exist, if so, delete them.
    log_files=( "$LOG_FILE" "$RSNAPSHOT_LOG_FILE" )
    for file in "${log_files[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
            log "Deleted logfile $file" "DEBUG"
        else
            log "$file doesn't exist. Next." "DEBUG"
        fi
    done
fi

log "*.backupper.sh start.*" "INFO"
log "Configfile => $CONFIG_FILE." "INFO"

# Check if a argument is provided.
if [ -z "$1" ]; then
    log "No argument supplied, fallback to config defined job => $DEFAULT_JOB." "WARNING"
    JOB="$DEFAULT_JOB"
else
    JOB="$1"
    log "Executed job => $JOB." "DEBUG"
fi

# Check if the second job is executed.
if [[ "$SEC_JOB" == "$JOB" ]]; then
    log "Second job got triggered, share has changed. [$SHARE => $SEC_SHARE]" "INFO"
    SHARE="$SEC_SHARE"
fi

# Try to mount the network drive.
i=0
while [[ $i < $TRIES ]]; do
    # TODO: Check if the mounting point exists!
    if ! grep -q "$MOUNT" /proc/mounts; then
        { # Try and mount the network drive.
            log "Mounting share ... [$SHARE]" "INFO"
            mount -t cifs -o username="$USER",password="$PASSWORD" "$SHARE" "$MOUNT" > /dev/null 2>&1
            log "Network share successfully mounted!" "INFO"
            break
        } || {
            (( i=i+1 ))
            log "[$i/$TRIES] Could not mount network share! ... [$SHARE -> $MOUNT]" "WARNING"
            if [[ i == $TRIES ]]; then
                log "Could not mount the network share $TRIES times!\nExiting script!" "ERROR"
                panic 1
            fi
        }
    else
        log "Network share is already mounted." "INFO"
        break
    fi
done

log "Starting rSnapshot job ... [$JOB]" "INFO"
{
    # Run the rsnapshot backup job.
    cmd="$RSNAPSHOT $JOB"
    output=`$cmd`   
    # Check if the rsnapshot output is empty or not.
    if [[ $output != "" ]]; then
        log "$output" "INFO"
    else
        log "rSnapshot didn't return any output." "WARNING"
    fi
} || {
    # Built a wrapper around a rsnapshot error that happens if a file changes while rsnapshot runs (return_val: 2).
    if [ $? -eq 0 ] -eq 2 ]; then
        log "Backup complete. No warnings/errors occured." "INFO"
    else
        log "rSnapshot retured with an error (code: $?), please check the rSnapshot logs for more information." "ERROR"
        panic 1
    fi
}

script_end=$(date +'%d.%m.%Y %T')
log "Start: $script_start :: End: $script_end" "DEBUG"
panic 0