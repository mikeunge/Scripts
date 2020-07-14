"""
    This is the default config file used for 'mailman.py'.

    When using mailman, delete the '.default' part from the file and change to real data.
    eg. config.default.py -> config.py
"""

mail = {
    "sender": {
        "name": "Test-Sender",
        "email": "status@test.com",
        "password": "testerabc123"
    },
    "receiver": {
        "name": "Status-Mail",
        "email": "status@test.com"
    },
    "attachments": {
        "1": "/var/log/rsnapshot.log",
        "2": "/var/log/backupper.log"
    }
}

config = {
    "mail": {
        "prefix": "[%status%]",
        "subject": "Test"
    },
    "server": {
        "smtp_server": "",
        "smtp_port": 587
    },
    "logging": {
        "path": "/var/log/mailman.log",
        "level": "INFO"
    },
    "template_default": "default",
    "template_path": "/script/mailman", # don't set '/' at the end of path!
    "max_attachment_size": "2000000"    # 2MB in Bytes
}