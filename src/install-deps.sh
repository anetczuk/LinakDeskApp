#!/bin/bash

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


### required for pygraphviz
#sudo apt install graphviz-dev


# ## ensure required version of pip3
# pip3 install --upgrade 'pip>=18.0'


## install requirements
PIP_ARGS=""
if [[ $* == *--break-system-packages* ]]; then
    PIP_ARGS="--break-system-packages"
fi
pip3 install $PIP_ARGS -r "$SCRIPT_DIR/requirements.txt"


echo
echo "installation done"
echo
