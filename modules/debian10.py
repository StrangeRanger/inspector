from modules.globalvar import *


def identifying_text(file):
    for line in file:
        fields = line.split()
        date_str = " ".join(fields[0:2]) + " "
        # Makes sure that the log date is correct; if current date is January 01
        # 2020 and looking a line in log with date Dec 31 that was logged in 2019,
        # the date would = Dec 31 2020. Lines below prevent this.
        try:
            date = datetime.strptime(date_str + str(this_year), "%b %d %Y").date()
            if date > today: raise DateError
        except DateError:
            date = datetime.strptime(date_str + str(last_year), "%b %d %Y").date()
        # Will skip any abnormal/non-regular text in /var/log/auth.log that could
        # produce an Error, and then prints out a message telling the user to check
        # out the line in the file.
        except ValueError:
            print("{}There was an abnormality in /var/log/auth.log: {}{}\n".format(cyan, line, defclr))
            continue

        if date < start_date:
            # Too old for interest
            continue
        # "user : TTY=tty/1 ; PWD=/home/user ; USER=root ; COMMAND=/bin/su"
        if fields[4] == "sudo:":
            user = fields[5]
            # Successful
            conditions = user != "root" and (fields[8] != "incorrect" and fields[8] != "NOT" if len(fields) >= 9 else None) and \
                         fields[-4] == "USER=root" and fields[-2] in ("COMMAND=/bin/su", "COMMAND=/usr/bin/su")
            # Unsuccessful
            conditions2 = user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and \
                          fields[-4] == "USER=root" and fields[-2] in ("COMMAND=/bin/su", "COMMAND=/usr/bin/su")
            # `sudo su`...
            conditions3 = fields[-3] == "USER=root" and fields[-1] in ("COMMAND=/bin/su", "COMMAND=/usr/bin/su")
            # `sudo -i` and `sudo bash` # D.1. purposefully separated from conditions3,
            # else when previous commands are used, the number of times a user attempts
            # to log into an account becomes twice as many as actual; without writing a
            # paragraph, this is due to what text is being looked for, and what is produced
            # when the commands above are (in this comment) are executed
            conditions35 = fields[-3] == "USER=root" and fields[-1] in ("COMMAND=/bin/bash", "COMMAND=/usr/bin/bash")

            # "..."; identifies users who are not in the sudoers file and tried to execute
            # a command with root privilege
            if user != "root" and (fields[8] == "NOT" and fields[10] == "sudoers" and fields[16] == "USER=root" and
                                   fields[18].startswith("COMMAND=") if len(fields) >= 9 else None):
                days[date]["~" + user] += 1
            # "..."; identifies users who successfully became root using `sudo bash` or `sudo -i` # D.1.
            if user != "root" and (fields[8] != "incorrect" if len(fields) >= 9 else None) and conditions35:
                # A.2. The defaultdict key becomes the date and its value, which is the
                # counter, is the user, which gains a plus 1 in the counter
                days[date]["+" + user] += 1
            # "..."; identifies users who unsuccessfully became root using `sudo bash`
            # or `sudo -i` # D.1.
            elif user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and conditions35:
                days[date]["*" + user] += int(fields[7])  # A.2.
            # "..."; identifies users who unsuccessfully became root using `sudo su`
            elif user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and conditions3:
                days[date]["*" + user] += int(fields[7])  # A.2.
            # "..."; identifies users who unsuccessfully became root using `sudo su root`
            elif conditions2 and fields[-1] == "root":
                days[date]["*" + user] += int(fields[7])  # A.2.
            # "..."; identifies users who unsuccessfully switched users using `sudo su <username>`
            elif conditions2 and fields[-1] != "root":
                victim = fields[19]
                daysv2[date]["/" + user][victim] += int(fields[7])  # B.2.

        if fields[4].startswith("su:"):
            # (to root) <username>
            conditions4 = fields[-4] == "root)" and fields[-3] != "root"
            # (to <victim_username>) <username>
            conditions5 = fields[-4] != "root)" and fields[-3] != "root"

            # "(to root) <username> on pts/<n>"; identifies users who've successfully
            # became root using `su`, `su root`, `sudo su`, or `sudo su root`
            if " ".join(fields[5:7]) == "(to root)" and conditions4:
                user = fields[-3]
                days[date]["+" + user] += 1 # A.2.
            # "FAILED SU (to root) <username> on pts/<n>"; identifies users who've
            # unsuccessfully became root using `su` and/or `su root`
            elif " ".join(fields[5:7]) == "FAILED SU" and conditions4:
                user = fields[-3]
                days[date]["*" + user] += 1 # A.2.
            # "(to <victim_username>) <username> on pts/<n>"; identifies users who've
            # successfully switched users using `su <victim_username>` or `sudo su <victim_username>`
            elif fields[5] == "(to" and conditions5:
                user = fields[-3]
                victim = fields[-4].replace(")", "")
                daysv2[date]["-" + user][victim] += 1  # B.2.
            # "FAILED SU (to <victim_username>) <username> on pts/<n>"; identifies users
            # who've unsuccessfully switched users using `su <victim_username>`
            elif " ".join(fields[5:7]) == "FAILED SU" and conditions5:
                user = fields[-3]
                victim = fields[-4].replace(")", "")
                daysv2[date]["/" + user][victim] += 1  # B.2.
