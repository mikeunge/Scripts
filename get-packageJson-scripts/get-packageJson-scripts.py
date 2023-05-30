#!/usr/bin/env python3
import os
import json

# PATHS defines what directories should get scanned for subdirs + package.json
PATHS = ['./packages/', './services/', './infrastructure/']

def has_package_json(dir):
    package_json = f'{dir}/package.json'
    return os.path.exists(package_json) and os.path.isfile(package_json)

def get_scripts(package):
    scripts = []
    f = open(package)
    data = json.load(f)
    f.close()
    try:
        for keys, _ in data['scripts'].items():
            scripts.append(keys)
    except:
        print(f'{package} does not contain scripts')
        return []
    return scripts

def update_script_index(scripts, update):
    if len(scripts) == 0:
        return update
    for u in update:
        if not u in scripts:
            scripts.append(u)
    return scripts

def main():
    packages = []
    scripts = []
    for p in PATHS:
        for dir in os.scandir(p):
            if dir.is_dir():
                if has_package_json(dir.path):
                    packages.append(f'{dir.path}/package.json')
    for package in packages:
        update = get_scripts(package)
        if len(update) > 0:
            scripts = update_script_index(scripts, update)
    print(f'\nScripts found in: {" ".join(str(x) for x in PATHS)}')
    for s in scripts:
        print(f'--> {s}')

if __name__ == '__main__':
    main()
