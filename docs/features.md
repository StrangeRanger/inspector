# Program Features and Notes

This script identifies users who have used sudo bash, sudo -i, sudo su, and su/su root

If a user on the system created a temporary account in order to log in as root, then deletes the account after he or she is done with it, the temporary account will still show up in the scan results.

Any and all users who use sudo su to change to another user will be marked/identified. This makes it easier to identify a user who tries to blame a different user for logging in as root. (see Script Notes/Faults below)

Any and all users who attempt to either log into the root account or switch users, and are unsuccessful, will be identified and marked down.

Users who are not in the sudoers file and try to execute a command with root privilege, will be identified.

