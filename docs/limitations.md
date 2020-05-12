# Inspector Limitations

## Falsely Blaming Users

If a user with sudo power, call him Mal, switches to another user who may or may not have sudo power, call him Vic, then uses sudo or su, will cause Vic to be blamed for executing the commands instead of Mal. Though, Mal must know Vic's password in order to successfully use sudo. The best way to verify who actually did it is

  * Semi-built in helper: Because the script will identify users who use su and sudo su, Mal will be identified as an individual who switched users.
  * Method of weeding out the true culprit: Look through the auth.log at the logs taken on the given day that the incident took place... To know what to look for, please refer to "identifying-patterns.odt"; it contains all auth.log logs that are created in relation to the given commands and there relative success or failure...

Affected Distributions:

* All officially supported linux distros

## `su <non-existent user>`

Due to a lack of logging to the system `auth.log`, if a user uses `su <username>` or `sudo su <username>`, where the username is a user that does not exist on the system, the program will not be able to report that a user tried to switch to another user on the system.

Affected Distributions:

* Debian 10.x

## What it doesn't do

The script will not identify the root user itself for anything, even if it does/meets the requirements/identifiers that are mentioned above. This means that if for some reason root changes to another user, the script will not identify root doing this.

