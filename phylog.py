#! python

import re
import time
from colorama import init

init()

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
    regex = r"\[[0-9\-a-zA-Z :\/]+\] PHP (\w+\s*\w*|\[[0-9]{3}\])"
    result = re.search(regex, message)
    if result:
        return result.group(1)
    else:
        return ""


def add_color(message, fg='white', bg='black', style='normal'):
    return '\x1b[' + str(font[style]) + ';' + str(font[fg]) + ';' + str(font[bg] + 10) + 'm' + message + '\x1b[0m'


def log(message):
    """
    :param message:
    :return: void
    """
    code = get_code(message)
    if code == '':
        print(add_color(message, 'cyan'))
    if code == 'Warning' or len(code) > 0 and code[0] == '3':
        print(add_color(message, 'yellow'))
    elif code == 'Fatal error' or len(code) > 0 and code[0] == '4':
        print(add_color(message, 'red'))
    elif code == 'Parse error' or len(code) > 0 and code[0] == '5':
        print(add_color(message, fg='red', style='bold'))
    else:
        print(add_color(message, 'cyan'))


def main():
    file = 'php.log'
    while True:
        try:
            f = f = open(file, 'r')
            break
        except FileNotFoundError:
            file = input('Please enter a file name: ')

    erase = input('Clear the file\'s contents?[Y/N]: ')
    if erase[0] and erase[0].lower() == 'y':
        f.close()
        f = f = open(file, 'w')
        f.close()
        print('File cleared.')
        f = f = open(file, 'r')

    while True:
        for line in f:
            if line:
                log(line)
        time.sleep(.1)


main()
