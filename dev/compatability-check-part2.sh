#!/bin/bash
#
# Default root, tester, and user password: asdf1234!@#$ASD
#
# IMPORTANT: This script needs more testing. Do you not rely on it for accurate
#            compatability checking.
#
################################################################################

echo "Creating temp user 'tester'..."
sudo adduser --quiet --gecos "" --home /home/tester --shell /bin/bash tester
echo "Create password for 'root' user..."
sudo passwd root


echo -e "\n\nPerforming incorrect password tests...\n"

echo "Command: 'su'"
su -c 'echo -e "Success";exit'
echo "Command: 'su root'"
su -c 'echo -e "Success";exit' root
echo "Command: 'su tester'"
su -c 'echo -e "Success";exit' tester
echo "Command: 'sudo su'"
sudo su -c 'echo -e "Success";exit'
echo "Command: 'sudo su root'"
sudo su  -c 'echo -e "Success";exit' root
echo "Command: 'sudo su tester'"
sudo su -c 'echo -e "Success";exit' tester
echo "Command: 'sudo -i'"
sudo -i bash -c 'echo -e "Success";exit'
echo "Command: 'sudo bash'"
sudo bash -c 'echo -e "Success";exit'


echo -e "\n\nPerforming correct password tests...\n"

echo "Command: 'su'"
su -c 'echo -e "Success";exit'
echo "Command: 'su root'"
su -c 'echo -e "Success";exit' root
echo "Command: 'su tester'"
su -c 'echo -e "Success";exit' tester
echo "Command: 'sudo su'"
sudo su -c 'echo -e "Success";exit'
echo "Command: 'sudo su root'"
sudo su  -c 'echo -e "Success";exit' root
echo "Command: 'sudo su tester'"
sudo su -c 'echo -e "Success";exit' tester
echo "Command: 'sudo -i'"
sudo -i bash -c 'echo -e "Success";exit'
echo "Command: 'sudo bash'"
sudo bash -c 'echo -e "Success";exit'


echo "Removing temp user..."
sudo deluser --remove-all-files tester 2>/dev/null
echo "Resetting root..."
sudo passwd -dl root
