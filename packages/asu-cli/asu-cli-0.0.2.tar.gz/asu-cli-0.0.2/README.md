# AWS S3 CLI utils (asu)

[![Test](https://github.com/tekumara/asu/actions/workflows/pythonapp.yml/badge.svg)](https://github.com/tekumara/asu/actions/workflows/pythonapp.yml)
[![PyPI version](https://badge.fury.io/py/asu-cli.svg)](https://pypi.org/project/asu-cli/)

## Usage

```
Usage: asu [OPTIONS] COMMAND [ARGS]...

  AWS S3 CLI utils

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  sse   List default encryption for all buckets
  tags  List tag for all buckets
```

## Install

Install the latest version using [pipx](https://github.com/pipxproject/pipx):

```
pipx install asu-cli
```

If you have previously installed asu, run `pipx upgrade asu-cli` to upgrade to the latest version.

## Development

### Prerequisites

- make
- node (required for pyright. Install via `brew install node`)
- python >= 3.7

### Getting started

To get started run `make install`. This will:

- install git hooks for formatting & linting on git push
- create the virtualenv in _./venv/_
- install this package in editable mode

Then run `make` to see the options for running checks, tests etc.

`. venv/bin/activate` activates the virtualenv. When the requirements in `setup.py` change, the virtualenv is updated by the make targets that use the virtualenv.
