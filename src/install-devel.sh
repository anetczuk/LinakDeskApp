#!/bin/bash

##
## Script installs package in "editable" mode (symlinks) into Python's user directory.
##

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


## creates "*.egg-info" directory along package dir

pip3 install --user -e "$SCRIPT_DIR" 

echo "Removing $SCRIPT_DIR/build direcotry"
rm -r "$SCRIPT_DIR/build"
