#! python

import re
import time
from colorama import init

# ANSI Escape colors
font = {
    "normal": 0,
    "bold": 1,
    "underline": 2,
    "negative1": 3,
    "negative2": 5,
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "purple": 35,
    "cyan": 36,
    "white": 37,
}


def get_code(message):
    # CodeIgniter
    regex = r"^([\w]+)"
    result = re.search(regex, message)
    if result:
        return result.group(1)
    else:
        return ""


def add_color(message, fg="white", bg="black", style="normal"):
    line = (
        "\x1b["
        + str(font[style])
        + ";"
        + str(font[fg])
        + ";"
        + str(font[bg] + 10)
        + "m"
        + message
        + "\x1b[0m"
    )
    # Remove the newline from the file so no blank lines will be printed
    line = line.replace("\n", "")
    return line


def log(message, *args, **kwargs):
    """
    :param message:
    :return: void
    """
    code = get_code(message)
    _args = []
    _kwargs = {}
    if code == "WARNING" or len(code) > 1 and code[1] == "3":
        _args.append("yellow")
    elif code == "ERROR" or len(code) > 1 and code[1] == "4":
        _args.append("red")
    elif code == "CRITICAL" or len(code) > 1 and code[1] == "5":
        _kwargs["fg"] = "red"
        _kwargs["style"] = "bold"
    elif code == "INFO" or code == "DEBUG":
        _args.append("green")
    else:
        _args = args
        _kwargs = kwargs
    print(add_color(message, *_args, **_kwargs))
    return _args, _kwargs


def main():
    init()
    # Try out default file names first
    files = ["logs/php.log"]
    file = "php.log"
    while True:
        try:
            f = open(file, "r")
            break
        except FileNotFoundError:
            # Prompt the user for a file if php.log doesn't exist
            if len(files) > 0:
                file = files.pop()
            else:
                file = input("Please enter a file name: ")

    # Allow the user to clear the file before using
    erase = input("Clear the file's contents?[Y/N]: ")
    if erase[0] and erase[0].lower() == "y":
        f.close()
        f = open(file, "w")
        f.close()
        print("File cleared.")
        f = open(file, "r")

    # Throw out existing lines
    f.readlines()

    while True:
        _args, _kwargs = [], {}
        for line in f:
            _args, _kwargs = log(line, *_args, **_kwargs)
        # Pause for 1/10 of a second so it won't use up the CPU so much
        # Results still appear as if they were instant
        time.sleep(0.01)


main()
