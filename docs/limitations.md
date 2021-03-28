# Inspector Limitations

There are unformtunatley some limitations to what inspector can do as a result of how many Linux Distributions are designed.

!!! Note

    For simplicity, the user who perfroms the actions (user who changed accounts), will be refered to as Mal. The user who had the actions performed against (user who was changed to), will be refered to as Vic.

## Falsely Blaming Users

If Mal has sudo perms and changes to Vic's account, then attempts to switch to _another_ user, Vic will end up being reported for that action, instead than the Mal.

Affected Distributions:

- Ubuntu 20.04, 18.04, and 16.04.
- Debian 10 and 9.

## Switching To a Non-Existent User

Due to a lack of logging to the system's `auth.log`, if Mal uses `su [username]` or `sudo su [username]`, where the username is a non-existent user, Inspector will not be able to identify that Mal attempted to switch to another account.

Affected Distributions:

- Ubuntu 20.04
- Debian 10

## Unsupported Shells

If Mal uses a shell that is not listed in `/etc/shells`, Inspector won't be able to tell that Mal did anything wrong. It's highly unlikely that this will cause any problems as this file is managed by the system, but if Mal somehow removes the shell that they used, Inspector won't be able to report them.
