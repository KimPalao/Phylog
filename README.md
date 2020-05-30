# Phylog

Phylog is a PHP console logger.
Inspired by [Morgan](https://www.npmjs.com/package/morgan) for Node.js,
this file watches your php error log file and prints out all incoming
logs


## How to run:

Copy the phylog.py to the directory containing your log file.
If your log file is named php.log, this will automatically read it. Else,
it will prompt you for the file name.

You can also choose to clear the file before using it.

To use this effectively, please add these lines to your .php files:

`ini_set("log_errors", 1);`

`ini_set("error_log", '../logs/php.log');`

`ini_set('display_errors', '../logs/php.log');`

The program will read lines and color those that are in this format:

[12-Jun-2018 21:43:34 Europe/Berlin] PHP Notice:  Hello world! in C:\Projects\test\index.php on line 10

Add this line to your php file if you want to log the response code. Works most effectively in a router script

~~error_log('PHP [' . http_response_code() . '] ' . $_SERVER['REQUEST_URI']);~~
`error_log('[' . http_response_code() . '] ' . $_SERVER['REQUEST_URI']);`

The program will then read the following line:

[12-Jun-2018 21:43:34 Europe/Berlin] [200]: /index in C:\Projects\test\index.php on line 10

Dependencies: colorama

## Changelog

##### 0.15
Changed the regular expression used so that logging the http response code without
the 'PHP' will still trigger the color

##### 0.14
Fixed a bug that would print a line twice if it didn't match the pattern