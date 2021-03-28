## Features

As of now, Inspector's features are fairly limited. Despite this, it has all the functionality needed to perform the task that it was set out to perfrom. Below is a list of notes and features that Inspector currently has.

1. To switch to root or another user's account, a user must execute one of several commands:

     ```bash
     su
     su root
     su [username]
     sudo su
     sudo su root
     sudo su [username]
     sudo -i
     sudo bash
     sudo [command]  # Specific to when the user executing the command doesn't have permission to use sudo
     ```

     Inspector is capable of identifying users who have attempted (successfully or otherwise) to use any of those commands.

2. Deleted user accounts who've attempted to switch users, will still be reported despite them not existing any more.
3. Inspector will report a user who attempted to switch to nonexistent account.
4. Users who do not have sudo perms that attempt to execute a command with root privilege, will be reported by Inspector.
