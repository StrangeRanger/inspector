# Inspector Limitations

## Falsely Blaming Users

If a malicious user with sudo power switches to a different user on the system, then attempts to switch to root or -another- user, the victim (the user who was initially switched to) will end up being blamed for the use that command/action, rather than the malicious user.

Below is a list of all the affected linux distributions:

- Ubuntu
    - 16.04
    - 18.04
    - 20.04
- Debian
    - 9
    - 10

## Switching To a Non-Existent User

Due to a lack of logging to the system's `auth.log`, if a user uses `su [username]` or `sudo su [username]`, where the username is a non-existent user on the system, the program will not be able to identify that a user attempted to switch to another account.

Below is a list of all the affected linux distributions:

- Ubuntu 20.04
- Debian 10

## Non-Supported Shells

If a malicious user uses a shell that inspector does not support, it is not possible to identify the user who become root or switched to another user. To check what shells Inspector supports on your system, use `sudo cat /etc/shells` in the terminal. This means that if a user installs a shell then removes it after doing what they are doing, they can not be identified.

## What It Doesn't Do

Inspector will not identify the root user for anything, even if any actions performed by root meet the capabilities of the program. This means that if for some reason, root changes to a different user, Inspector will not identify root as doing so.
