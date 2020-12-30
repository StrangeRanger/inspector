# Inspector

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Maintenance](https://img.shields.io/maintenance/yes/2020)](https://github.com/StrangeRanger/inspector/graphs/commit-activity)
[![Documentation Status](https://readthedocs.org/projects/inspector-project/badge/?version=latest)](https://inspector-project.readthedocs.io/en/latest/?badge=latest)
[![GPLv2 license](https://img.shields.io/badge/License-GPLv2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)

Inspector is a security tool with the purpose of identifying users who have both successfully and unsuccessfully switched to root or another user linux based distributions.

For more information on Inspector, please visit https://inspector-project.readthedocs.io/en/latest

## Getting Started

### Requirements

- python 3.x
- distro

### Installing Dependencies

To install all of the dependencies for Inspector, run the following command: `python3 -m pip install -r requirements.txt`

## Officially Supported Linux Distributions

| Distributions | Distro Versions |
|---------------|-----------------|
| Ubuntu        | 16.04<br>18.04<br>20.04 |
| Debian        | 9<br>10         |

## Supported Shells

When a user becomes root or switches to another user, the kind of shell the user was using is detailed in the log. This shell must be one that is currently listed in inpsector's code. Below is a list of all the current shells that inspector supports/can detect

- bash
- sh
- zsh
- *More to be added*
