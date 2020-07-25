# Inspector Limitations

## Falsely Blaming Users

If a malicious user with sudo power switches to another user on the system, then attempts to switch to root or another user on the system, the victim (the user who was logged into) will end up be blamed for the use that command/action, rather than the malicious user.

### Affected Distributions

Below is a list of all the linux distributions affected by this limitation:

* Ubuntu 16.04
* Ubuntu 18.04
* Debian 9
* Debian 10

## Switching To a Non-Existent User

Due to a lack of logging to the system's `auth.log`, if a user uses `su [username]` or `sudo su [username]`, where the username is a non-existent user on the system, the program will not be able to identify that a user attempted to switch to another account on the system.

### Affected Distributions

Below is a list of all the linux distributions affected by this limitation:

* Debian 10

## What it doesn't do

The program will not identify the root user itself for anything, even if it does/meets the requirements/identifiers that are mentioned above. This means that if for some reason root changes to another user, the script will not identify root doing this.
