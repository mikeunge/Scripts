#!/bin/usr/python3
# -*- coding: utf-8 -*-
#
# backupper.py
# version: 1.0.2
# build: alpha
#
# Author:	Ungerböck Michele
# Github:	github.com/mikeunge
# Company:	GEDV GmbH
#
# All rights reserved.
#
import os
import sys
import logging
import subprocess
try:    # check if the config.py exists
    from config import network, config
except ImportError:
    print("Could not find the configuration (config.py) file. - Please make sure the file exists and then try running again.")
    send_mail("error")
    sys.exit(1)


class Backup:
    def __init__(self, job):
        self.tries = int(config['mount_tries'])
        self.job = job
        self.credentials = {"user": network['user'], "password": network['password']}
        self.share = network['share']
        self.mount_point = network['mount']


    def mount_share(self):
        """
            Try to mount the network drive.

            Return: True/False
                If the mounting wasn't successfully, it returns with false.
                This causes a fatal error because the backup cannot execute further.
        """
        i = 0
        proc_cmd = f"cat /proc/mounts | grep {self.share} > /dev/null 2>&1"
        mount_cmd = f"mount -t cifs -o username={self.credentials['user']},password={self.credentials['password']} {self.share} {self.mount_point} > /dev/null 2>&1"
        while i <= self.tries:
            if os.system(proc_cmd) == 0:
                # Check if the share is already mounted.
                logger.info(f"Network drive already mounted. [{self.share}]")
                return True
            logger.info(f"Trying to mount [{self.share}] -> [{self.mount_point}]. ({str(i)}/{str(self.tries)})")
            if os.system(mount_cmd) == 0:
                return True
            else:
                # Try again..
                logger.error(f"Couldn't mount the network drive. ({str(i)}/{str(self.tries)})")
                i += 1
        return False


    def start(self):
        if not self.mount_share():
            logger.fatal(f"Coulnd't mount the network drive. - Check if the share exists and the credentials are correct.")
            send_mail("error")
            sys.exit(1)
        # Start the actual backup job.
        rsnapshot = config['rsnapshot_path']
        result = subprocess.run([rsnapshot, self.job], capture_output=True)
        if not result.returncode == 0:
            logger.fatal(f"rsnapshot exited with an error:\n{str(result.stderr, 'utf-8')}")
            send_mail("errors")
        else:
            logger.info(f"rsnapshot ({self.job}): OK!")
            send_mail("success")
        sys.exit(0)


def send_mail(status):
    # Send a status mail via mailman.py
    script_path = config['mailman_path']
    if not os.path.exists(script_path):     # make sure it exists
        err_msg = f"Couldn't send mail; Script [mailman.py] not found! - Make sure the script is located in: {script_path}. Exiting."
        print(err_msg)
        logger.critical(err_msg)
        sys.exit(1)     # Exits with error.
    # Check if a correct status is used/set.
    if (status.lower() != "success") or (status.lower() != "warning") or (status.lower() != "error"):
        # If not, set the default to warning.
        status == "warning"
    subprocess.run(["sudo", "python3", script_path, status])


# Function for creating the logger and setting the correct log_level.
def setup_logger(level, path):
    # Change the logging format below..
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    try:
        # Check the different cases, default: DEBUG
        if level.upper() == "DEBUG":
            logging.basicConfig(filename=path, level=logging.DEBUG, format=log_format)
        elif level.upper() == "INFO":
            logging.basicConfig(filename=path, level=logging.INFO, format=log_format)
        elif level.upper() == "WARNING":
            logging.basicConfig(filename=path, level=logging.WARNING, format=log_format)
        elif level.upper() == "ERROR":
            logging.basicConfig(filename=path, level=logging.ERROR, format=log_format)
        else:
            logging.basicConfig(filename=path, level=logging.DEBUG, format=log_format)
        return logging.getLogger()
    except Exception as ex:
        print(f"Could not setup the logger, exiting the program. - Error: {ex}")
        send_mail("error")
        sys.exit(1)


if __name__ == '__main__':
    logger = setup_logger(config['log_level'], config['log_path'])
    try:
        arg_job = sys.argv[1]
        logger.info(f"Passed argument/job to execute: {arg_job}")
    except IndexError as ix:
        arg_job = config['default_job']  # load the defined default from config.
        logger.warning(f"No argument found, fallback to default: {arg_job}")
    backup = Backup(arg_job)
    backup.start()
