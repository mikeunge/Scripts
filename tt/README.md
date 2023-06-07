# TT

> __tt - the simple timetrace wrapper__

## Why

I wanted to track my time spent on wroking on projects, I stumbled across the wonderfull tool called [_timetrace_](https://github.com/dominikbraun/timetrace). It is sleek, written in go and the commands are simple and intuitive, but there is one issue - you cannot stop/resume your last tracking task.

So, I built a wrapper for it.
I also would love a feature to automatically detect if I'm working or not - so - I built a daemon that detects if I'm logged in or not (_utilizes gnome tho_).

## Installation

### Prerequisite

- timetrace - [dominikbraun/timetrace](https://github.com/dominikbraun/timetrace)
- ubuntu/gnome (_used by the daemon_)

### Installing tt & daemon

After that it is as simple as running ```bash install.sh```.
The files will be moved into __/usr/bin/__ and ```tt``` should be available from your terminal.

Now, instead of using ```timetrace``` - run all your commands using ```tt```!
tt parses all the commands and forwards them to _timetrace_, on the first run, tt invokes the _daemon_ so the lock/unlock of the PC gets catched.
