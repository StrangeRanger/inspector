# Program Notes

1. To switch to root or another user's account, a user has to execute one of several commands. Inspector is capable of identifying users who have attempted to switch to root or another user's account via:

    * su
    * su root
    * su [username]
    * sudo su
    * sudo su root
    * sudo su [username]
    * sudo -i
    * sudo bash
    * sudo [command]
        * Specific to when the user executing the command doesn't have permission to use sudo

2. Even if an account was deleted after it had either switched to root or another user on the system, the program will still be able to identify it.
3. The program will identify users who are not in the sudoers file (don't have perms to use sudo) that attempt to execute a command with root privilege.
