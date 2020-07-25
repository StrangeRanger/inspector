# Program Features and Notes

Here is a list of features and notes about the program, that haven't already been explained:

* To switch to root or another user's account, a user has to execute one of several commands. Inspector is capable of identifying users who have attempted to switch to root or another user's account via:
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
* Even if an account was deleted after either switch to root or another user on the system, it will still be identified.
* The program will identify users who are not in the sudoers file (don't have perms to use sudo) and try to execute a command with root privilege.
