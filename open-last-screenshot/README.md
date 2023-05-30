# Open Last Screenshot

__Open your last created screenshot (_or any image for that matter_) right from the terminal!__

## But why?

I use the termnial for most of my tasks, from basic file editing to running programs - it's my swiss knife and tool of choice.
The need for this script came when I needed to write some files or simply wanted to check something, but I'm pretty lazy and always looking for the latest screenshot so I can open it was tideous.

## Information

As the tile suggest, this script opens the latest screenshot.
The script is pretty simple and straight forward, you provide it with the path where all the screenshots get stored as well as the path to the binary that should open the image.

### Prerequisite

I only tested it on Linux, Windows user _might_ run into some issues.

- [Python3](https://www.python.org/downloads/)
- [Feh](https://github.com/derf/feh) (_or an image previewer of your choice_)

### Configuration

To configure it, simply open the python file with your text editor of choice, change the screenshot directory as well as the binary path for previewing it to fit your needs.
After that, simply run it - it should work right out of the box.

I use ```feh``` as my image preview programm of choice - it's simple and lightweight, but you can use everything what you prefer.
