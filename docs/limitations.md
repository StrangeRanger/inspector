# Inspector Limitations

## Falsely Blaming Users

If a user with sudo power, call him Mal, switches to another user who may or may not have sudo power, call him Vic, then uses sudo or su, will cause Vic to be blamed for executing the commands instead of Mal. Though, Mal must know Vic's password in order to successfully use sudo. The best way to verify who actually did it is

  * Semi-built in helper: Because the script will identify users who use su and sudo su, Mal will be identified as an individual who switched users.
  * Method of weeding out the true culprit: Look through the auth.log at the logs taken on the given day that the incident took place... To know what to look for, please refer to "identifying-patterns.odt"; it contains all auth.log logs that are created in relation to the given commands and there relative success or failure...

## Check if these are actually true

Due to the system's lack of output, if a user tries to log into an account via su <username>, the script will not be able to identify that individual as bad user.

Due to how the script (has to) identifies users if a user inputs their sudo password correctly when executing sudo su <username>, but the username does not exist, they will not be marked at all.

## What it doesn't do

The script will not identify the root user itself for anything, even if it does/meets the requirements/identifiers that are mentioned above. This means that if for some reason root changes to another user, the script will not identify root doing this.

