network = {
    "user": "admin",
    "password": "admin",
    "share": "//192.168.0.1/data",
    "mount": "/mnt/"
}

config = {
    "rsnapshot_path": "/usr/bin/rsnapshot",     # define where rsnapshot is located
    "mailman_path": "/scripts/mailman/mailman.py",
    "mount_tries": "3",
    "default_job": "daily",
    "log_level": "info",
    "log_path": "/var/log/backupper.log"
}