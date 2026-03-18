#!/bin/bash

##
## Script installs copy of package into Python's user directory.
##

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


## creates "*.egg-info" and "build" directory along package dir

if [[ $* == *--system* ]]; then
    pip3 install "$SCRIPT_DIR" 
else
    pip3 install --user "$SCRIPT_DIR" 
fi

echo "Removing $SCRIPT_DIR/build direcotry"
rm -r "$SCRIPT_DIR/build"
rm -r "$SCRIPT_DIR"/*.egg-info
