#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

DEBUG=True
SCREENSHOT_PATH="/home/mike/Pictures/Screenshots"
IMAGE_PREVIEW_BIN="/usr/bin/feh"
ALLOWED_EXTENSIONS=["jpg", "jpeg", "png", "gif"]

def pprint(msg, is_error=False):
    if DEBUG or is_error:
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} :: {msg}")

def file_exists(path):
    return os.path.exists(path) and os.path.isfile(path)

def get_last_screenshot(files):
    newest_file = ""
    newest_creation_time = 0.0
    for file in files:
        creation_time = os.path.getctime(file)
        if creation_time > newest_creation_time:
            newest_creation_time = creation_time
            newest_file = file
    return newest_file

def build_path(path, file):
    if path.split("/")[len(path.split("/"))-1] != "/":
        return f"{path}/{file}"
    else:
        return f"{path}{file}"

def get_all_images(path):
    images = []
    for p in os.scandir(path):
        if not p.is_file():
            pprint(f"{p.name} is not a file")
        else:
            file = p.name
            ext = file.split(".")[len(file.split("."))-1]
            if ext in ALLOWED_EXTENSIONS:
                images.append(build_path(path, file))
            else:
                pprint(f"{file} is not allowed (ALLOWED_EXTENSIONS_EXCEPTION)")
    return images

def open_screenshot(path, bin):
    subprocess.Popen([bin, f'{path}'])

def main():
    if not file_exists(IMAGE_PREVIEW_BIN):
        pprint(f"Could not get image preview '{IMAGE_PREVIEW_BIN}', exiting", True)
        exit(-1)
    images = get_all_images(SCREENSHOT_PATH)
    if len(images) == 0:
        pprint(f"No images found in {SCREENSHOT_PATH}, exiting", True)
        exit(1)
    last_image = get_last_screenshot(images)
    open_screenshot(last_image, IMAGE_PREVIEW_BIN)

if __name__ == "__main__":
    main()
