# Inspector

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![GPLv2 license](https://img.shields.io/badge/License-GPLv2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
![Repo Size](https://img.shields.io/github/repo-size/StrangeRanger/inspector)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Inspector is a security tool with the purpose of identifying users who have both successfully and unsuccessfully switched to root or another user linux based distributions.

## Getting Started

### Installing Dependencies

To install dependencies for Inspector, run either of the following commands: 
- `python3 -m pip install -r requirements.txt` (installs globally)
- `pipenv install -r requirements.txt` (installs locally via pipenv)
    - pipenv must already be installed: `python3 -m pip install pipenv`

## Officially Supported Linux Distributions

| Distributions | Distro Versions |
|---------------|-----------------|
| Ubuntu        | 20.04<br>16.04<br>18.04 |
| Debian        | 10<br>9        |
