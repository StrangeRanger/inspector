#!/usr/bin/env python3

"""
The main file that performs the task set by the project.
"""
####[ Imports ]#########################################################################


from sys import exit
from os import geteuid
from datetime import timedelta
from pkg import RED, GREEN, DEFCLR, today, days, daysv2, start_date


####[ Pip imports ]#####################################################################


try:
    import distro
except ImportError:
    exit(
        "{}'distro' is not installed and is required to run this program{}\n"
        "\nExiting...".format(RED, DEFCLR)
    )


####[ Post Import Variables ]###########################################################


distribution = distro.id()
distro_version = distro.version(pretty=False, best=False)


####[ Functions ]#######################################################################


def get_count_info():
    """Access the items inside counter, which contains the victims/users who were
    switched to.
    """
    for victim, counter in count.items():
        victim_sentence_end = str(counter) + (
            " time" + DEFCLR if counter == 1 else " times" + DEFCLR
        )
        print("     {} {} {}".format(RED, victim, victim_sentence_end))


def unsupported():
    exit(
        "{}Distro ID: {}\n"
        "Distro Version: {}\n\n"
        "Your operating system is not supported by inspector{}\n\n"
        "Exiting...".format(RED, distribution, distro_version, DEFCLR)
    )


####[ Prepping ]########################################################################
#### Verifies that the Linux Distribution is supported by inspector.


## Checks to see if the program was executed with root privilege.
if geteuid() != 0:
    exit(
        "{}Please run this program as or with root privilege{}\n\n"
        "Exiting...".format(RED, DEFCLR)
    )

## Check for if running on supported Linux distribution.
if distribution == "ubuntu":
    if distro_version in ("16.04", "18.04"):
        from pkg.distro_specific import debian9_ubuntu16 as identifying_text
    elif distro_version == "20.04":
        from pkg.distro_specific import debian10_ubuntu20 as identifying_text
    else:
        unsupported()
elif distribution == "debian":
    if distro_version == "9":
        from pkg.distro_specific import debian9_ubuntu16 as identifying_text
    elif distro_version == "10":
        from pkg.distro_specific import debian10_ubuntu20 as identifying_text
    else:
        unsupported()
else:
    unsupported()


####[ Main ]############################################################################


# Looks through "auth.log.1" if starting date is not located in "auth.log" then
# continues through "auth.log".
# TODO: Add a way to reach even older auth.log's
with open("/var/log/auth.log", "r") as file:
    identifying_text(file)
    if start_date.strftime("On %b %d:").replace(" 0", "  ") not in file:
        try:
            with open("/var/log/auth.log.1", "r") as file2:
                identifying_text(file2)
        except IOError:
            pass

while start_date <= today:
    users = days[start_date]
    victims = daysv2[start_date]

    print(start_date.strftime("On %b %d:"))
    if users:
        for user, count in users.items():
            user_sentence_end = str(count) + (
                " time" + DEFCLR if count == 1 else " times" + DEFCLR
            )

            if "~" in user:
                print(
                    "{}   {} is not in the sudoers file and tried to execute a"
                    "command with root privilege {}".format(
                        RED, user, user_sentence_end
                    )
                )
            elif "+" in user:
                print("{}   {} became root {}".format(RED, user, user_sentence_end))
            elif "*" in user:
                print(
                    "{}   {} tried to become root {}".format(
                        RED, user, user_sentence_end
                    )
                )
    else:
        print("{}   No one became root{}".format(GREEN, DEFCLR))

    if victims:
        for user, count in victims.items():
            if "-" in user:
                print("{}   {} switched to".format(RED, user))
                get_count_info()
            elif "/" in user:
                print("{}   {} tried to switch to".format(RED, user))
                get_count_info()
    else:
        print("{}   No one switched users{}".format(GREEN, DEFCLR))

    start_date += timedelta(days=1)
