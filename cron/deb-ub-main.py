import sys
import os.path
import collections
from datetime import datetime, timedelta

class DateError(Exception):
    pass

N = 0 # number of days that will be checked that came before today: N = 1 means that today's and yesterday's logs will be checked
path = os.path.split(sys.argv[0])[0] + ("root-login-search.log" if os.path.isfile("root-login-search-cronjob.py") else "/root-login-search.log") # ensures the correct location of root-login-log
log = open(path, "a")

os.chmod(path, 0000) 
log.write("---auth.log scanned on " + str(datetime.now()) + "---\n")
#print("---auth.log scanned on " + str(datetime.now()) + "---\n") # C.1. part of message that will be sent by email if smtp is enabled

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
                log.write("***There was an abnormality in /var/log/auth.log: {}***\n".format(line))
                #print("***There was an abnormality in /var/log/auth.log: {}***".format(line)) # C.1.
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
                    days[date]["*" + user] += 1 # A.2.
                # "..."; identifies users who successfully became root using `sudo su root`
                elif conditions and fields[-1] == "root":
                    days[date]["+" + user] += 1 # A.2.
                # "..."; identifies users who unsuccessfully became root using `sudo su root`
                elif conditions2 and fields[-1] == "root":
                    days[date]["*" + user] += 1 # A.2.
                # "..."; identifies users who successfully switched users using `sudo su <username>`
                elif conditions and fields[-1] != "root": 
                    victim = fields[14]
                    daysv2[date]["-" + user][victim] += 1 # B.2.
                # "..."; identifies users who unsuccessfully switched users using `sudo su <username>`
                elif conditions2 and fields[-1] != "root":
                    victim = fields[19]
                    daysv2[date]["/" + user][victim] += 1 # B.2.

            if fields[4].startswith("su["):
                # root by <username>
                conditions4 = fields[-3] == "root" and fields[-1] != "root"
                # <username> by <username>
                conditions5 = fields[-3] != "root" and fields[-1] != "root"

                ### when a way is found, make it so that the severity level is greater with the ones below. "Change your password...<> knows your password"
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
            end_of_sentence = str(counter) + (" time\n" if counter == 1 else " times\n")
            #end_of_sentence_print = str(counter) + (" time" if counter == 1 else " times") # C.1.
            log.write("      " + victim + " " + end_of_sentence)
            #print("     ", victim, end_of_sentence_print) # C.1.

    while start_date <= today:
        log.write(start_date.strftime("On %b %d:\n"))
        #print(start_date.strftime("On %b %d:")) # C.1.
        users = days[start_date]
        victims = daysv2[start_date]
        
        # A.3.
        if users:
            for user, count in users.items(): # user, count is used because we're reading from a counter; which is a dict that maps username to count of occurrences
                end_of_sentence = str(count) + (" time\n" if count == 1 else " times\n")
                #end_of_sentence_print = str(count) + (" time" if count == 1 else " times") # C.1.
                
                if "~" in user:
                    log.write("   " + user + " is not in the sudoers file and tried to execute a command with root privilege " + end_of_sentence)
                    #print("  ", user, "is not in the sudoers file and tried to execute a command with root privilege", end_of_sentence_print) # C.1.
                elif "+" in user:
                    log.write("   " + user + " became root " + end_of_sentence)
                    #print("  ", user, "became root", end_of_sentence_print) # C.1.
                elif "*" in user:
                    log.write("   " + user + " tried to become root " + end_of_sentence)
                    #print("  ", user, "tried to become root", end_of_sentence_print) # C.1.
        else:
            log.write("   No one became root\n")
            #print("   No one became root") # C.1.

        # B.3.
        if victims:
            for user, count in  victims.items():
                if "-" in user:
                    log.write("   " + user + " switched to\n")
                    #print("  ", user, "switched to") # C.1.
                    section_two()
                elif "/" in user:
                    log.write("   " + user + " tried to switch to\n")
                    #print("  ", user, "tried to switch to") # C.1.
                    section_two()
        else:
            log.write("   No one switched users\n")
            #print("   No one switched users") # C.1.

        start_date += timedelta(days=1)

    log.write("+-*/+-*/+-*/+-*/+-*/+-*/+-*/+-*/+-*/+-*/+-*/+-*/+-*/+-*/\n" if users or victims else "*****************************************************\n")
    
root_users()
log.close()
