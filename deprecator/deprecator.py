#!/usr/bin/env python3
import os
import subprocess

ROOT=os.getcwd()
PATH="libs-frontend/"
NOT_TO_DEPRECATE=["eslint-config", "common", "html2pdf-client", "haxios", "job-ats-interface", "helpers", "config", "node-ts-cache", "db-connection", "axios-rate-limit"]


# @returns [[full_dir_path, dir_name], [..., ...], ...]
def get_folder_packages(path):
    packages = []
    for package in os.listdir(path):
        dir = os.path.join(path, package)
        if os.path.isdir(dir):
            packages.append(package)
    return packages


def deprecate(package, message):
    res = subprocess.run(["npm", "deprecate", f"@hokify/{package}", f'"{message}"'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return res.returncode


def restrict_access(package):
    res = subprocess.run(["npm", "access", "restricted", f"@hokify/{package}"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return res.returncode


def main():
    packages = get_folder_packages(PATH)
    for package in packages:
        if not package in NOT_TO_DEPRECATE:
            status_code = restrict_access(package)
            if status_code != 0:
                print(f"Could not restrict access '{package}'")
            else:
                print(f"Restricted '{package}'")
            status_code = deprecate(package, f"{package} is no longer public, please use workspace protocol!")
            if status_code != 0:
                print(f"Could not deprecate '{package}'")
            else:
                print(f"Deprecated '{package}'")
        else:
            print(f"Not deprecating '{package}' because it is still needed")


if __name__ == "__main__":
    print(f"Starting depreaction from: {ROOT}\n")
    main()

