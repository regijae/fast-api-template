#!/usr/bin/env bash

set -e
set -x

mypy app
ty check app
ruff check app scripts
ruff format app scripts --check
