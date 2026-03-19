#!/bin/bash

##
## Script installs copy of package into Python's user directory.
##

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
ROOT_DIR=$(realpath "$SCRIPT_DIR/..")


if [[ $* == *--system* ]]; then
    pip3 install "$ROOT_DIR"
else
    pip3 install --user "$ROOT_DIR"
fi
