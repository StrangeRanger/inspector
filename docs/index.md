# Introduction

Inspector is a security tool with the purpose of identifying users who have both successfully and unsuccessfully switched to root or another user on the system. It does this by looking for specific logs that are written to `/var/log/auth.log`.

!!! Note
    For information on what kinds of logs that the program looks for, read the [Dev Documentation](dev-docs/index.md).

## Getting Started

Inspector has one dependency that you will need to install via pip. To do this, execute this command in the project's root directory: `python3 -m pip install -r requirements.txt`
