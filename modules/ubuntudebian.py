from modules.globalvar import *

def identifying_text(file): 
    for line in file:
        fields = line.split() 
        date_str = " ".join(fields[0:2]) + " " 
        # makes sure that the log date is correct; if current date is January 01 2020 and looking a line in log with date Dec 31 that was logged in 2019, the date would = Dec 31 2020. Lines below prevent this.
        try:
            date = datetime.strptime(date_str + str(this_year), "%b %d %Y").date()
            if date > today: raise DateError
        except DateError:
            date = datetime.strptime(date_str + str(last_year), "%b %d %Y").date()
        # will skip any abnormal/non-regular text in /var/log/auth.log that could produce an Error, and then prints out a message telling the user to check out the line in the file.
        except ValueError:
            print("{}There was an abnormality in /var/log/auth.log: {}{}\n".format(cyan, line, defclr))
            continue

        if (date < start_date):
            # too old for interest
            continue 
        # "user : TTY=tty/1 ; PWD=/home/user ; USER=root ; COMMAND=/bin/su"
        if fields[4] == "sudo:":
            user = fields[5]
            # successful
            conditions = user != "root" and (fields[8] != "incorrect" and fields[8] != "NOT" if len(fields) >= 9 else None) and fields[-4] == "USER=root" and fields[-2] == "COMMAND=/bin/su"
            # unsuccessful
            conditions2 = user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and fields[-4] == "USER=root" and fields[-2] == "COMMAND=/bin/su"
            # `sudo su`...
            conditions3 = fields[-3] == "USER=root" and fields[-1] in ("COMMAND=/bin/bash", "COMMAND=/bin/sh", "COMMAND=/bin/su")

            # "..."; identifies users who are not in the sudoers file and tried to execute a command with root privilege
            if user != "root" and (fields[8] == "NOT" and fields[10] == "sudoers" and fields[16] == "USER=root" and fields[18].startswith("COMMAND=") if len(fields) >= 9 else None):
                days[date]["~" + user] += 1
            # "..."; identifies users who successfully became root using `sudo su`
            if user != "root" and (fields[8] != "incorrect" if len(fields) >= 9 else None) and conditions3:
                days[date]["+" + user] += 1 # A.2. The defaultdict key becomes the date and its value, which is the counter, is the user, which gains a plus 1 in the counter
            # "..."; identifies users who unsuccessfully became root using `sudo su`
            elif user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and conditions3:
                days[date]["*" + user] += int(fields[7]) # A.2.
            # "..."; identifies users who successfully became root using `sudo su root`
            elif conditions and fields[-1] == "root":
                days[date]["+" + user] += 1 # A.2.
            # "..."; identifies users who unsuccessfully became root using `sudo su root`
            elif conditions2 and fields[-1] == "root":
                days[date]["*" + user] += int(fields[7]) # A.2.
            # "..."; identifies users who successfully switched users using `sudo su <username>`
            elif conditions and fields[-1] != "root": 
                victim = fields[14]
                daysv2[date]["-" + user][victim] += 1 # B.2. 
            # "..."; identifies users who unsuccessfully switched users using `sudo su <username>`
            elif conditions2 and fields[-1] != "root":
                victim = fields[19]
                daysv2[date]["/" + user][victim] += int(fields[7]) # B.2.

        if fields[4].startswith("su["):
            # root by <username>
            conditions4 = fields[-3] == "root" and fields[-1] != "root"
            # <username> by <username>
            conditions5 = fields[-3] != "root" and fields[-1] != "root"

            # "Successful su for root by <username>"; identifies users who've successfully became root using `su` and/or `su root`
            if fields[5] == "Successful" and conditions4:
                user = fields[-1]
                days[date]["+" + user] += 1 # A.2.
            # "FAILED su for root by <username>"; identifies users who've unsuccessfully became root using `su` and/or `su root`
            elif fields[5] == "FAILED" and conditions4:
                user = fields[-1]
                days[date]["*" + user] += 1 # A.2.
            # "Successful su for <username> by <username>"; identifies users who've successfully switched users using `su <username>`
            elif fields[5] == "Successful" and conditions5:
                user = fields[-1]
                victim = fields[-3]
                daysv2[date]["-" + user][victim] += 1 # B.2. 
            # "FAILED su for <username> by <username>"; identifies users who've unsuccessfully switched users using `su <username>`
            elif fields[5] == "FAILED" and conditions5:
                user = fields[-1]
                victim = fields[-3]
                daysv2[date]["/" + user][victim] += 1 # B.2.