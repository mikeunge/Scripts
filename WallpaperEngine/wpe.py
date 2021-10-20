#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, json
from os import walk, path, system
from random import randint

# check if DEBUG is set
DEBUG = False
if len(sys.argv) > 1:
    DEBUG = True in [ x == 'debug' for x in sys.argv]


# dbg(msg: str)
#
# @desc     Print the provided message if DEBUG is enabled.
def dbg(msg: str):
    if DEBUG:
        print(f'[debug] {msg}')


# get_wallpaper(wp_path: str, extension: tuple) -> list[str]
#
# @desc     Loads all the files inside the provided folder path and returns a list.
#
# @params   wp_path     -> path where the wallpapers are located
#           extensions  -> tuple of file extensions to use
#
# @return   list[str]   -> array with all the images
def get_wallpapers(wp_path: str, extensions: tuple) -> list:
    for (_, _, filenames) in walk(wp_path):
        wp = [wp_path + file for file in filenames if file.endswith(extensions)]
    return wp


# set_wallpaper(wallpaper: str)
#
# @desc     Set the provided wallpaper (uses feh)self.
#
# @params   wallpaper   -> full path to the wallpaper
def set_wallpaper(wallpaper: str):
    # if wallpaper has whitespaces, make it linux (feh) friendly
    wallpaper = wallpaper.replace(" ", "\\ ")
    dbg(f'Setting wallpaper: {wallpaper}')
    system(f'feh --bg-scale {wallpaper}')


# load_config(file: str) -> dict
#
# @desc     Load the configuration file.
#
# @params   file    -> path to config file
#
# @return   dict    -> filled config dict or empty dict if nothing was found
def load_config(file: str) -> dict:
    dbg(f'Loading config: {file}')
    try:
        with open(file, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f'Could not load config file ({file}).\nError: {e}')
        config = {}
    return config 


# check_remember_list(file: str, wp: str) -> bool
# 
# @desc     Check the remember file if we can use the provided wallpaper.
#
# @params   file    -> path to the remember file
#           wp      -> wallpaper to check
#
# @return   bool    -> True if wp exists, False if not
def check_remember_list(file: str, wp: str) -> bool:
    if not path.isfile(file):
        dbg(f'File ({file}) does not exist')
        return False
    with open(file, 'r') as f:
        data = f.read().split(';')
        for index, item in enumerate(data):
            if item == wp:
                dbg(f'Wallpaper already used: {index} - {item}')
                return True
    return False


# append_remember_list(file: str, wp: str) -> int
#
# @desc     Add a new element to the remember file, or create the file if it doesn't exist.
#
# @params   file    -> path to the remember file
#           wp      -> wallpaper to write
#
# @return   int     -> count of items 
def append_remember_list(file: str, wp: str) -> int:
    if path.isfile(file):
        with open(file, 'r+') as f:
            data = f.read()
            f.seek(0, 0)
            f.write(wp.rstrip('\r\n') + ';' + data)
        dbg(f'Write {wp} to file {file} was a success')
    else:
        # if the file does not exist, we create it and write to it
        with open(file, 'w') as f:
             print(wp, file=f)
        dbg(f'File {file} successfully created')
    with open(file, 'r') as f:
        data = f.read().split(';')
    return len(data)-1


# pop_remember_list(file: str, max: int, cur: int)
#
# @desc     Remove the last entry of the file.
#
# @params   file    -> path to remember file
#           max     -> how many are allowed in the file
#           cur     -> current in the file
def pop_remember_list(file: str, max: int, cur: int):
    if cur <= max:
        return
    if not path.isfile(file):
        dbg(f'Nothing to pop, file ({file}) does not exist.')
        return
    with open(file, 'r') as f:
        data = f.read().split(';')
    with open(file, 'w') as f:
        for item in data[:-2]:
            f.write(item+';')
    dbg(f'Removed {data[len(data)-2]} successfully from {file}')
    # recursive function, so if the max changed we get to remove all the overhead
    pop_remember_list(file, max, cur-1)


# serialize_path(arg_path: str) -> str
#
# @desc     Serialize the provided path
#
# @params   arg_path-> path to serialize
#
# @return   str     -> the serialized path
def serialize_path(arg_path: str) -> str:
    if arg_path[0] == '~':
        return arg_path = path.expanduser(arg_path)
    return arg_path


# main(conf: dict)
#
# @desc     The main function, this manages the behaviour of this app.
#
# @params   config  -> config dict
def main(conf: dict):
    conf['wp_path'] = serialize_path(conf['wp_path'])
    conf['remember_path'] = serialize_path(conf['remember_path'])
    wallpapers = get_wallpapers(conf['wp_path'], tuple(conf['extensions']))
    if len(wallpapers) <= 0:
        print('No wallpapers found.')
        return
    if conf['random']:
        while True:
            wallpaper = wallpapers[randint(0, len(wallpapers)-1)]
            if not check_remember_list(conf['remember_path'], wallpaper):
                set_wallpaper(wallpaper)
                cur_list_lines = append_remember_list(conf['remember_path'], wallpaper)
                pop_remember_list(conf['remember_path'], conf['remember'], cur_list_lines)
                break
        return
    if not path.isfile(conf['wp']):     # check if wp is already a valid path
        wp = path.join(conf['wp_path'], conf['wp'])
    # check if the desired wallpaper is in the returned list
    if wp in wallpapers:
        set_wallpaper(wp)
    else:
        # if we cannot find the image, we set random to true and run the script again
        dbg(f'Wallpaper ({conf["wp"]}) not found, selecting random image')
        conf['random'] = True
        main(conf)


if __name__ == '__main__':
    config_paths = ['wpe.json', '~/.config/wpe.json', '~/.config/wpe/wpe.json']
    config = {}
    for c in config_paths:
        c = serialize_path(c)
        if path.isfile(c):
            config = load_config(c)
            break
    if config == {}:    # if the config is empty, use fallback config
        config = {
            'wp_path': '~/Pictures/Wallpaper/',     # make sure to add the trailing slash
            'wp': '',                               # if you want a fixed wp, enter the name here
            'random': True,                         # set this to 'False' if you want to used a fixed wp
            'remember': 5,                          # how many iterations should we remember your last set wallpaper(s)
            'remember_path': '~/.wpe_store',        # the path where we remember the set wallpapers
            'extensions': [                         # enter the file extensions to use
                '.jpg',
                '.png',
                '.webp',
                '.gif'
            ]
        }
    # check if user specifies a wallpaper path via args
    if len(sys.argv) > 1 and (sys.argv[1] == '--set' or sys.argv[1] == '-s'):
        try:
            wp = sys.argv[2]
            config['wp'] = wp
            config['random'] = False
            dbg(f'Changing wp to {wp} - disable random')
        except IndexError as ix:
            dbg(f'Error: {ix}')
    dbg(f'Config dump: {config}')
    main(config)
