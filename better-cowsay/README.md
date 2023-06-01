# Better Cowsay

__If you like cowsay, you will love better-cowsay!__

## Information

Better-Cowsay is a simple wrapper that chooses a random _cowfile_ on each invocation (_it's super fun_).

### Available commands

```sh
  -h  --help      Print help information
  -v  --version   Prints the version
  -d  --debug     Enable debug logging
  -c  --config    Specify the configuration path
  -f  --filename  Specify the cowfile name
```

## Install

Before you start, make sure you have [go](https://www.go.dev) installed!

To build & install better-cowsay, simply run ```bash ./make install``` - this builds the binary and and moves all the needed files where they belong.

__What gets created?__

- configfile -> ~/.config/better-cowsay.json
- cowfiles -> ~/.conwfiles/
- better-cowsay -> /usr/bin/better-cowsay

_You can always edit the paths, simply change the variables in the ```make``` script._

### Prerequisite

- Golang (_used for building_)

## Todo

- [ ] Provide the cowfile name you want to execute
