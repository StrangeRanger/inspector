# Introduction

Inspector is a security tool with the purpose of identifying users who have both successfully and unsuccessfully switched to root or another user on linux based distributions. It does this by looking for specific logs that are written to `/var/log/auth.log`.

!!! Note
    For information on what logs the program looks for, read the [Dev Documentation](dev-docs/index.md).
