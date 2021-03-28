# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.1] - 2021-03-27

### Changes

- Updated README.md
- Updated Documentation

### Fixes

- Re-definition found for builtin function PYL-W0622 (@deepsourcebot)
- from module import \* used; unable to detect undefined names PYL-W0401 (@deepsourcebot)
- Unused import from wildcard import found PYL-W0614 (@deepsourcebot)
- Consider using in PYL-R1714 (@deepsourcebot)
- Module imported but unused PYL-W0611 (@deepsourcebot)
- Undefined name detected PYL-E0602 (@deepsourcebot)

## [2.1.0] - 2021-02-05

### Added

- Officially supports Ubuntu 20.04
- Relies on `/etc/shells` to know what shells Inspector should keep track of
- Scripts that test compatibility

### Changed

- Documentation changes
- Styled using [black](https://github.com/psf/black)

## [2.0.0] - 2020-07-26

### Added

- If ran without root privilege, users will be notified and the program will exit
- Will present Distro ID and a version number if run on an unsupported distribution/OS

### Changed

- Moved documentation to mkdocs, which is now hosted on readthedocs.org
- Moved the identifying pattern files (now called identifying logs) to mkdocs on readthedocs.org
- Merged what used to be two different branches for different operating systems, into the same branch
  - Code that is required for specific operating systems will be imported based on what operating system program is being run on
- Removed cron scripts till they can be properly implemented
- Updated code to better follow personal and PEP style guide

### Fixed

- A few small bugs

[unreleased]: https://github.com/StrangeRanger/inspector/compare/v2.1.1...HEAD
[2.1.1]: https://github.com/StrangeRanger/inspector/releases/tag/v2.1.1
[2.1.0]: https://github.com/StrangeRanger/inspector/releases/tag/v2.1.0
[2.0.0]: https://github.com/StrangeRanger/inspector/releases/tag/v2.0.0
