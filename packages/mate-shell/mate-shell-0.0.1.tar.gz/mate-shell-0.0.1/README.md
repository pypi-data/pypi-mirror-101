# Mate: Extremely pluggable and modular shell
[![build](https://github.com/twisted-fun/mate/actions/workflows/python-package.yml/badge.svg)](https://github.com/twisted-fun/mate/actions/workflows/python-package.yml)
[![](https://img.shields.io/github/license/twisted-fun/mate?logo=github)](https://github.com/twisted-fun/mate/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/twisted-fun/mate/branch/master/graph/badge.svg?token=AIQF2UVD8B)](https://codecov.io/gh/twisted-fun/mate)
[![](https://img.shields.io/github/last-commit/twisted-fun/mate?logo=github)](https://github.com/twisted-fun/mate/commits/master)
[![](https://img.shields.io/badge/sentry-active-brightgreen)](https://sentry.io/organizations/r00t3r/projects/)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=twisted-fun_mate&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=twisted-fun_mate)
## Features
- Easy plugin creation using setuptools
- Manage group of plugins better by `mate --shells`
- Built-in auto complete
- Forced modularity in plugins
- Dope looking shell
- Provides command output redirect to embedded ipython
- Supports batch executions by `mate --exec`

## Installation
### Using git
```bash
git clone https://github.com/twisted-fun/mate.git
cd mate
pip3 install -e .
```

## Usage
```
$ mate --help
usage: mate [-h] [-V] [--debug] [-p PROJECT_DIR] [-o OUTPUT_DIR] [-s SOCKET] [--shells SHELLS] [--exec EXEC]

optional arguments:
  -h, --help            Show this help message
  -V, --version         Show version number
  --debug               Set console log level to DEBUG.
  -p PROJECT_DIR, --project-dir PROJECT_DIR
                        Specify root directory of a project for analysis.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Specify root directory to store various result files.
  -s SOCKET, --socket SOCKET
                        Provide [Protocol]Host[:Port] of a service for analysis.
  --shells SHELLS       Specify setuptools group names separated by comma to fetch plugins instead of default 'mate'.
  --exec EXEC           Provide mate shell command for batch execution.
```
