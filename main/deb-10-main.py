import collections
from datetime import datetime, timedelta

class DateError(Exception):
    pass

N = 8 # number of days that will be checked that came before today: N = 1 means that today's and yesterday's logs will be checked
red = "\033[1;31m"
cyan  = "\033[1;36m"
green = "\033[0;32m"
defclr = "\033[0m"

def root_users():
    today = datetime.now().date()
    start_date = today - timedelta(days=N)
    this_year = datetime.now().year
    last_year = this_year - 1
    days = collections.defaultdict(collections.Counter) # A.1. a defaultdict that maps objects (dates and users) to a counter
    daysv2 = collections.defaultdict(lambda: collections.defaultdict(collections.Counter)) # B.1. two nested defaultdicts that map objects (dates, users, and victims) to a counter

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
                conditions = user != "root" and (fields[8] != "incorrect" and fields[8] != "NOT" if len(fields) >= 9 else None) and fields[-4] == "USER=root" and fields[-2] in ("COMMAND=/bin/su", "COMMAND=/usr/bin/su")
                # unsuccessful
                conditions2 = user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and fields[-4] == "USER=root" and fields[-2] in ("COMMAND=/bin/su", "COMMAND=/usr/bin/su")
                # `sudo su`...
                conditions3 = fields[-3] == "USER=root" and fields[-1] in ("COMMAND=/bin/su", "COMMAND=/usr/bin/su")
                # `sudo -i` and `sudo bash` # D.1. purpousfully seperated from conditions3, else when previous commands are used, the number of times a user attemps to log into an account becomes twice as many as actual; without writing a paragaph, this is due to what text is being looked for, and what is produced when the commands above are (in this comment) are executed)
                conditions35 = fields[-3] == "USER=root" and fields[-1] in ("COMMAND=/bin/bash", "COMMAND=/usr/bin/bash")

                # "..."; identifies users who are not in the sudoers file and tried to execute a command with root privilege
                if user != "root" and (fields[8] == "NOT" and fields[10] == "sudoers" and fields[16] == "USER=root" and fields[18].startswith("COMMAND=") if len(fields) >= 9 else None):
                    days[date]["~" + user] += 1
                # "..."; identifies users who successfully became root using `sudo bash` or `sudo -i` # D.1.
                if user != "root" and (fields[8] != "incorrect" if len(fields) >= 9 else None) and conditions35:
                    days[date]["+" + user] += 1 # A.2. The defaultdict key becomes the date and its value, which is the counter, is the user, which gains a plus 1 in the counter 
                # "..."; identifies users who unsuccessfully became root using `sudo bash` or `sudo -i` # D.1.
                elif user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and conditions35:
                    days[date]["*" + user] += int(fields[7]) # A.2.
                # "..."; identifies users who unsuccessfully became root using `sudo su`
                elif user != "root" and (fields[8] == "incorrect" if len(fields) >= 9 else None) and conditions3:
                    days[date]["*" + user] += int(fields[7]) # A.2.
                # "..."; identifies users who unsuccessfully became root using `sudo su root`
                elif conditions2 and fields[-1] == "root":
                    days[date]["*" + user] += int(fields[7]) # A.2.
                # "..."; identifies users who unsuccessfully switched users using `sudo su <username>`
                elif conditions2 and fields[-1] != "root":
                    victim = fields[19]
                    daysv2[date]["/" + user][victim] += int(fields[7]) # B.2.

            if fields[4].startswith("su:"):
                # (to root) <username>
                conditions4 = fields[-4] == "root)" and fields[-3] != "root" 
                # (to <victim_username>) <username>
                conditions5 = fields[-4] != "root)" and fields[-3] != "root"

                # "(to root) <username> on pts/<n>"; identifies users who've successfully became root using `su`, `su root`, `sudo su`, or `sudo su root`
                if " ".join(fields[5:7]) == "(to root)" and conditions4:
                    user = fields[-3]
                    days[date]["+" + user] += 1 # A.2.
                # "FAILED SU (to root) <username> on pts/<n>"; identifies users who've unsuccessfully became root using `su` and/or `su root`
                elif " ".join(fields[5:7]) == "FAILED SU" and conditions4:
                    user = fields[-3]
                    days[date]["*" + user] += 1 # A.2.
                # "(to <victim_username>) <username> on pts/<n>"; identifies users who've successfully switched users using `su <victim_username>` or `sudo su <victim_username>`
                elif fields[5] == "(to" and conditions5:
                    user = fields[-3]
                    victim = fields[-4].replace(")", "")
                    daysv2[date]["-" + user][victim] += 1 # B.2. 
                # "FAILED SU (to <victim_username>) <username> on pts/<n>"; identifies users who've unsuccessfully switched users using `su <victim_username>`
                elif " ".join(fields[5:7]) == "FAILED SU" and conditions5:
                    user = fields[-3]
                    victim = fields[-4].replace(")", "")
                    daysv2[date]["/" + user][victim] += 1 # B.2.

    
    # looks through "auth.log.1" if starting date is not located in "auth.log" then continues through "auth.log"
    with open("/var/log/auth.log", "r") as txt:
        identifying_text(txt)
        if start_date.strftime("On %b %d:").replace(" 0", "  ") not in txt:
            try:
                with open("/var/log/auth.log.1", "r") as txt1:
                    identifying_text(txt1)   
            except IOError:
                None            

    def section_two():
        for victim, counter in count.items(): # need to access the items inside count, which contains the victims/users who were switched to
            end_of_sentence = str(counter) + (" time" + defclr if counter == 1 else " times" + defclr)
            print("     {} {} {}".format(red, victim, end_of_sentence))

    while start_date <= today:
        print(start_date.strftime("On %b %d:"))
        users = days[start_date]
        victims = daysv2[start_date]

        # A.3.
        if users: 
            for user, count in users.items(): # user, count is used because we're reading from a counter, which is a dict that maps username to count of occurrences
                end_of_sentence = str(count) + (" time" + defclr if count == 1 else " times" + defclr)

                if "~" in user:
                    print("{}   {} is not in the sudoers file and tried to execute a command with root privilege {}".format(red, user, end_of_sentence))
                elif "+" in user:
                    print("{}   {} became root {}".format(red, user, end_of_sentence))
                elif "*" in user:
                    print("{}   {} tried to become root {}".format(red, user, end_of_sentence))
        else:
            print("{}   No one became root{}".format(green, defclr))

        # B.3.
        if victims:
            for user, count in  victims.items():
                if "-" in user:
                    print("{}   {} switched to".format(red, user))
                    section_two()
                elif "/" in user:
                    print("{}   {} tried to switch to".format(red, user))
                    section_two()
        else:
            print("{}   No one switched users{}".format(green, defclr))

        start_date += timedelta(days=1)

root_users()
