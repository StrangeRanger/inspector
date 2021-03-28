# Inspector

<!-- Active status commented out
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
-->

[![Project Tracker](https://img.shields.io/badge/repo%20status-Project%20Tracker-lightgrey)](https://randomserver.xyz/project-tracker.html)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CodeFactor](https://www.codefactor.io/repository/github/strangeranger/inspector/badge)](https://www.codefactor.io/repository/github/strangeranger/inspector)

Inspector is a security tool with the purpose of identifying users who have both successfully and unsuccessfully switched to root or another user on Linux based Distributions. It does this by scanning through `/var/log/auth.log` for specific patterns that indicate specific actions/executed commands.

## Getting Started

### Prerequisites

Install the required dependencies using either of the following commands:

- `python3 -m pip install -r requirements.txt` (installs globally)
- `pipenv install -r requirements.txt` (installs locally via pipenv)

### Installing

All you need to do is download the repository. There are no binaries or anything to install.

`git clone https://github.com/StrangeRanger/inspector/`

## Usage

Because Inspector needs to access `/var/log/auth.log`, you'll be required to execute Inspector with root priviledge:

`sudo python3 inspector.py`

## Supported Distributions

The following is a list of all the Linux Distributions that Inspector officially supports and works on:

| Distributions | Distro Versions         |
| ------------- | ----------------------- |
| Ubuntu        | 20.04<br>16.04<br>18.04 |
| Debian        | 10<br>9                 |
