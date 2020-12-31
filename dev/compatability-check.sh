#!/bin/bash

###
###
### Default root, tester, and user password: asdf1234!@#$ASD
###
###

green=$'\033[0;32m'
cyan=$'\033[0;36m'
red=$'\033[1;31m'
nc=$'\033[0m'

echo "Creating temp user 'tester'..."
sudo adduser --quiet --gecos "" --home /home/tester --shell /bin/bash tester
echo "Create password for 'root' user..."
sudo passwd root


echo -e "\n\nPerforming incorrect password tests...\n"

echo "${cyan}Provide incorrect password${nc}"
echo "Command: 'su'"
su
echo "${cyan}Provide incorrect password${nc}"
echo "Command: 'su root'"
su root
echo "${cyan}Provide incorrect password${nc}"
echo "Command: 'su tester'"
su tester
echo "${cyan}Provide incorrect password${nc}"
echo "Command: 'sudo su'"
sudo su
echo "${cyan}Provide incorrect password${nc}"
echo "Command: 'sudo su root'"
sudo su root
echo "${cyan}Provide incorrect password${nc}"
echo "Command: 'sudo su tester'"
sudo su tester
echo "${cyan}Provide incorrect password${nc}"
echo "Command: 'sudo -i'"
sudo -i
echo "${cyan}Provide incorrect password${nc}"
echo "Command: 'sudo bash'"
sudo bash


echo -e "\n\nPerforming correct password tests...\n"

echo "${cyan}Provide correct password${nc}"
echo "Command: 'su'"
su
echo "${cyan}Provide correct password${nc}"
echo "Command: 'su root'"
su root
echo "${cyan}Provide correct password${nc}"
echo "Command: 'su tester'"
su tester
echo "${cyan}Provide correct password${nc}"
echo "Command: 'sudo su'"
sudo su
echo "${cyan}Provide correct password${nc}"
echo "Command: 'sudo su root'"
sudo su root
echo "${cyan}Provide correct password${nc}"
echo "Command: 'sudo su tester'"
sudo su tester
echo "${cyan}Provide correct password${nc}"
echo "Command 'sudo su nonexistentuser'"
sudo su nonexistentuser
echo "${cyan}Provide correct password${nc}"
echo "Command: 'sudo -i'"
sudo -i
echo "${cyan}Provide correct password${nc}"
echo "Command: 'sudo bash'"
sudo bash


echo "Removing temp user..."
sudo deluser --remove-all-files tester 2>/dev/null
echo "Resetting root..."
sudo passwd -dl root