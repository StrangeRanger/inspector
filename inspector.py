#!/usr/bin/env python3

################################################################################
#
# [ Importing and class class creation ]
#
################################################################################

from modules.globalvar import *


class DateError(Exception):
    pass


################################################################################
#
# [ Variables ]
#
################################################################################

RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
DEFCLR = "\033[0m"


################################################################################
#
# [ Prepping ]
#
# Verifies that the python package "distro" is installed, then checks what
# distro the program is running on
#
################################################################################

try:
    import distro
except ImportError:
    exit("{}'distro' is not installed and is required to run this program{}\n"
         "\nExiting...".format(RED, DEFCLR))

distribution = distro.id()
distro_version = distro.version(pretty=False, best=False)

if distribution == "ubuntu":
    if distro_version == "16.04":
        from modules.distro_specific import debian9_ubuntu16 as identifying_text
        supported = True
    elif distro_version == "18.04":
        from modules.distro_specific import debian9_ubuntu16 as identifying_text
        supported = True
    elif distro_version == "20.04":
        from modules.distro_specific import debian10_ubuntu20 as identifying_text
        supported = True
    else:
        supported = False
elif distribution == "debian":
    if distro_version == "9":
        from modules.distro_specific import debian9_ubuntu16 as identifying_text
        supported = True
    elif distro_version == "10":
        from modules.distro_specific import debian10_ubuntu20 as identifying_text
        supported = True
    else:
        supported = False
else:
    supported = False

if not supported:
    exit("{}Distro ID: {}\n"
         "Distro Version: {}\n\n"
         "Your operating system is not supported by inspector{}\n\n"
         "Exiting...".format(RED, distribution, distro_version, DEFCLR))

# Checks to see if this script was executed with root privilege
if geteuid() != 0:
    exit("{}Please run this script as root or with root privilege{}\n\n"
         "Exiting...".format(RED, DEFCLR))


################################################################################
#
# [ Functions ]
#
################################################################################

def section_two():
    """
    Accesses the items inside count, which contains the victims/users who were
    switched to
    """
    for victim, counter in count.items():
        end_of_sentence = str(counter) + (" time" + DEFCLR if counter == 1 else
                                          " times" + DEFCLR)
        print("     {} {} {}".format(RED, victim, end_of_sentence))


################################################################################
#
# [ Main ]
#
################################################################################

# Looks through "auth.log.1" if starting date is not located in "auth.log" then
# continues through "auth.log"
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
        # 'user, count' is used because we're reading from a counter, which is a dict that maps
        # username to count of occurrences
        for user, count in users.items():
            end_of_sentence = str(count) + (" time" + DEFCLR if count == 1 else
                                            " times" + DEFCLR)

            if "~" in user:
                print("{}   {} is not in the sudoers fdile and tried to execute a"
                      "command with root privilege {}".format(RED, user, end_of_sentence))
            elif "+" in user:
                print("{}   {} became root {}".format(RED, user, end_of_sentence))
            elif "*" in user:
                print("{}   {} tried to become root {}".format(RED, user, end_of_sentence))
    else:
        print("{}   No one became root{}".format(GREEN, DEFCLR))

    # B.3.
    if victims:
        for user, count in  victims.items():
            if "-" in user:
                print("{}   {} switched to".format(RED, user))
                section_two()
            elif "/" in user:
                print("{}   {} tried to switch to".format(RED, user))
                section_two()
    else:
        print("{}   No one switched users{}".format(GREEN, DEFCLR))

    start_date += timedelta(days=1)
