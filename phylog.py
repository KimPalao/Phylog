#! python

import re
import time
from colorama import init

# ANSI Escape colors
font = {
    'normal': 0,
    'bold': 1,
    'underline': 2,
    'negative1': 3,
    'negative2': 5,
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'purple': 35,
    'cyan': 36,
    'white': 37,
}


def get_code(message):
    # a regular expression to match the following:
    # [12-Jun-2018 21:43:34 Europe/Berlin] PHP Notice:  Hello world! in C:\Projects\test\index.php on line 10
    # [12-Jun-2018 21:43:34 Europe/Berlin] PHP [200]:  / in C:\Projects\test\index.php on line 10
    regex = r'\[[0-9\-a-zA-Z :\/]+\] PHP (\w+\s*\w*|\[[0-9]{3}\])'
    result = re.search(regex, message)
    if result:
        return result.group(1)
    else:
        return ""


def add_color(message, fg='white', bg='black', style='normal'):
    line = '\x1b[' + str(font[style]) + ';' + str(font[fg]) + ';' + str(font[bg] + 10) + 'm' + message + '\x1b[0m'
    # Remove the newline from the file so no blank lines will be printed
    line = line.replace('\n', '')
    return line


def log(message):
    """
    :param message:
    :return: void
    """
    code = get_code(message)
    if code == 'Warning' or len(code) > 1 and code[1] == '3':
        print(add_color(message, 'yellow'))
    elif code == 'Fatal error' or len(code) > 1 and code[1] == '4':
        print(add_color(message, 'red'))
    elif code == 'Parse error' or len(code) > 1 and code[1] == '5':
        print(add_color(message, fg='red', style='bold'))
    else:
        print(add_color(message, 'cyan'))


def main():
    init()
    # Try out a default file name first
    file = 'php.log'
    while True:
        try:
            f = open(file, 'r')
            break
        except FileNotFoundError:
            # Prompt the user for a file if php.log doesn't exist
            file = input('Please enter a file name: ')

    # Allow the user to clear the file before using
    erase = input('Clear the file\'s contents?[Y/N]: ')
    if erase[0] and erase[0].lower() == 'y':
        f.close()
        f = open(file, 'w')
        f.close()
        print('File cleared.')
        f = open(file, 'r')

    while True:
        for line in f:
            log(line)
        # Pause for 1/10 of a second so it won't use up the CPU so much
        # Results still appear as if they were instant
        time.sleep(.1)


main()
