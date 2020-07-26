# Inspector Limitations

## Falsely Blaming Users

If a malicious user with sudo power switches to a different user on the system, then attempts to switch to root or another user, the victim (the user who was initially switched to) will end up being blamed for the use that command/action, rather than the malicious user.

Below is a list of all the affected linux distributions:

* Ubuntu
    * 16.04
    * 18.04
* Debian
    * 9
    * 10

## Switching To a Non-Existent User

Due to a lack of logging to the system's `auth.log`, if a user uses `su [username]` or `sudo su [username]`, where the username is a non-existent user on the system, the program will not be able to identify that a user attempted to switch to another account.

Below is a list of all the affected linux distributions:

* Debian 10

## What it doesn't do

Inspector will not identify the root user for anything, even if any actions performed by root meet the capabilities of the program. This means that if for some reason, root changes to a different user, Inspector will not identify root as doing so.
