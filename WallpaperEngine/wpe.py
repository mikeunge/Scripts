#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, json
from os import walk, path, system
from random import randint

# check if DEBUG is set
DEBUG = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        DEBUG = True


# dbg :: print debug messages
def dbg(msg):
    if DEBUG:
        print(f'[debug] {msg}')


# get_wallpaper :: takes the path where the wallpapers are stored and returns an array with all the available items.
def get_wallpapers(wp_path):
    wp = []
    for (_, _, filenames) in walk(wp_path):
        wp = [wp_path + file for file in filenames]
    return wp


# set_wallpaper :: sets the wallpaper, as param it needs the FULL path to the wallpaper.
def set_wallpaper(wallpaper):
    # if wallpaper has whitespaces, make it linux (feh) friendly
    wallpaper = wallpaper.replace(" ", "\\ ")
    dbg(f'setting wallpaper: {wallpaper}')
    system(f'feh --bg-scale {wallpaper}')


# load_config :: load a configuration file.
def load_config(file):
    dbg(f'loading config: {file}')
    try:
        with open(file, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f'Could not load config file ({file}).\nError: {e}')
        config = {}
    return config 


def main(conf):
    # expand the wp_path to an absolute path
    if conf['wp_path'][0] == '~':
        conf['wp_path'] = path.expanduser(conf['wp_path'])
    wallpapers = get_wallpapers(conf['wp_path'])
    if len(wallpapers) <= 0:
        print('No wallpapers found.')
        return
    if conf['random']:
        set_wallpaper(wallpapers[randint(0, len(wallpapers)-1)])
        return
    # check if the desired wallpaper is in the returned list
    wp = path.join(conf['wp_path'], conf['wp'])
    if wp in wallpapers:
        set_wallpaper(wp)
    else:
        # if we cannot find the image, we set random to true and run the script again
        dbg(f'wallpaper ({conf["wp"]}) not found, selecting random image')
        conf['random'] = True
        main(conf)


if __name__ == '__main__':
    config_paths = ['wpe.json', '~/.config/wpe.json', '~/.config/wpe/wpe.json']
    config = {}
    for c in config_paths:
        if c[0] == '~':
            c = path.expanduser(c)
        if path.isfile(c):
            config = load_config(c)
            break
    if config == {}:
        config = {
            'wp_path': '~/Pictures/Wallpaper/',  # make sure to add the trailing slash
            'wp': '',   # if you want a fixed wp, enter the name here
            'random': True,    # set this to 'False' if you want to used a fixed wp
        }
    # check if user specifies a wallpaper path via args
    if len(sys.argv) < 1: 
        if sys.argv[1] == '--set' or sys.argv[1] == '-s':
            try:
                wp = sys.argv[2]
                if path.isfile(wp):
                    config['wp'] = wp
                    config['random'] = False
                else:
                    print('Please provide a valid wallpaper and make sure you provide the full path to it.')
                    exit(1)
            except Exception as ex:
                print('Sorry but something is wrong with your wallpaper path. Please try again. :)')
                dbg(f'Error: {ex}')
                exit(1)
    dbg(f'config dump: {config}')
    main(config)
