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
    }
}

config = {
    "mail": {
        "prefix": "[Backup]",
        "subject": "Test"
    },
    "server": {
        "smtp_server": "",
        "smtp_port": 587
    },
    "logging": {
        "file": "mailman.log",
        "level": "INFO"
    }
}