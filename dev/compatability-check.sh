#!/bin/bash
#
# Default root, tester, and user password: asdf1234!@#$ASD
#
################################################################################

CYAN=$'\033[0;36m'
NC=$'\033[0m'

echo "Creating temp user 'tester'..."
sudo adduser --quiet --gecos "" --home /home/tester --shell /bin/bash tester
echo "Create password for 'root' user..."
sudo passwd root


echo -e "\n\nPerforming incorrect password tests...\n"

echo "${CYAN}Provide incorrect password${NC}"
echo "Command: 'su'"
su
echo "${CYAN}Provide incorrect password${NC}"
echo "Command: 'su root'"
su root
echo "${CYAN}Provide incorrect password${NC}"
echo "Command: 'su tester'"
su tester
echo "${CYAN}Provide incorrect password${NC}"
echo "Command: 'sudo su'"
sudo su
echo "${CYAN}Provide incorrect password${NC}"
echo "Command: 'sudo su root'"
sudo su root
echo "${CYAN}Provide incorrect password${NC}"
echo "Command: 'sudo su tester'"
sudo su tester
echo "${CYAN}Provide incorrect password${NC}"
echo "Command: 'sudo -i'"
sudo -i
echo "${CYAN}Provide incorrect password${NC}"
echo "Command: 'sudo bash'"
sudo bash


echo -e "\n\nPerforming correct password tests...\n"

echo "${CYAN}Provide correct password${NC}"
echo "Command: 'su'"
su
echo "${CYAN}Provide correct password${NC}"
echo "Command: 'su root'"
su root
echo "${CYAN}Provide correct password${NC}"
echo "Command: 'su tester'"
su tester
echo "${CYAN}Provide correct password${NC}"
echo "Command: 'sudo su'"
sudo su
echo "${CYAN}Provide correct password${NC}"
echo "Command: 'sudo su root'"
sudo su root
echo "${CYAN}Provide correct password${NC}"
echo "Command: 'sudo su tester'"
sudo su tester
echo "${CYAN}Provide correct password${NC}"
echo "Command 'sudo su nonexistentuser'"
sudo su nonexistentuser
echo "${CYAN}Provide correct password${NC}"
echo "Command: 'sudo -i'"
sudo -i
echo "${CYAN}Provide correct password${NC}"
echo "Command: 'sudo bash'"
sudo bash


echo "Removing temp user..."
sudo deluser --remove-all-files tester 2>/dev/null
echo "Resetting root..."
sudo passwd -dl root
