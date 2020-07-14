#!/bin/usr/python3
# -*- coding: utf-8 -*-
#
# routine.py
# version: 1.0.0
# build: alpha
#
# Author:	Ungerböck Michele
# Github:	github.com/mikeunge
# Company:	GEDV GmbH
#
# All rights reserved.
#
# This script checks if defined logs exist and moves/renames them.
#
import os
import sys
from datetime import datetime

log_paths = [
    "/var/log/backupper.log",
    "/var/log/rsnapshot.log"
]


def main():
    for x in log_paths:
        if os.path.exists(x):
            print(f"Renaming {x} ...")
            res = os.system(f"mv {x} {x}.{datetime.now.strftime('%H:%M:%S_%d-%m-%Y')}")
            if res != 0:
                print(f"Couldn't rename {x}!")
        else:
            print(f"{x} - does not exist.")
    print("done.")


if __name__ == '__main__':
    main()
    sys.exit(0)
