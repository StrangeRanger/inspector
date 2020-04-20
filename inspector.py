#!/usr/bin/python3

###############################################################################
#
# Creating a class
#
###############################################################################
#
from modules.globalvar import *

class DateError(Exception):
    pass

#
###############################################################################
#
# [ Variables ]
#
###############################################################################
#
red = "\033[1;31m"
cyan = "\033[1;36m"
green = "\033[0;32m"
defclr = "\033[0m"

#
###############################################################################
#
# Verifying if the python package "distro" is installed then checks what
# distro the program is running on
#
###############################################################################
#
try:
    import distro
except ImportError:
    exit("{}'distro' is not installed and is required to run this program{}\n\nExiting...".format(red, defclr))

distribution = distro.id()
distro_version = distro.version(pretty=False, best=False)

if distribution == "ubuntu":
    if distro_version == "16.04":
        from modules.ubuntudebian import *
        supported = True
    elif distro_version == "18.04":
        from modules.ubuntudebian import *
        supported = True
    else:
        supported = False
elif distribution == "deian":
    if distro_version == "9":
        from modules.debian10 import *
        supported = True
    elif distro_version == "10":
        from modules.debian10 import *
        supported = True
    else:
        supported = False
else:
    supported = False

if not supported:
    # TODO: uncomment and delete import when ready to use for real
    #exit("{}Your operating system is not supported by inspector{}\n\nExiting...".format(red, defclr)) TODO: uncomment when ready to use
    from modules.debian10 import *

#
###############################################################################
#
# [ Functions ]
#
###############################################################################
#
def section_two():
    # Need to access the items inside count, which contains the victims/users who were switched to
    for victim, counter in count.items():
        end_of_sentence = str(counter) + (" time" + defclr if counter == 1 else " times" + defclr)
        print("     {} {} {}".format(red, victim, end_of_sentence))

#
###############################################################################
#
# [ Main ]
#
###############################################################################        
#
# looks through "auth.log.1" if starting date is not located in "auth.log" then continues through "auth.log"
with open("/var/log/auth.log", "r") as txt:
    identifying_text(txt)
    if start_date.strftime("On %b %d:").replace(" 0", "  ") not in txt:
        try:
            with open("/var/log/auth.log.1", "r") as txt1:
                identifying_text(txt1)   
        except IOError:
            None

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
