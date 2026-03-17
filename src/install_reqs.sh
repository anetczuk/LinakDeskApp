#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


cd $SCRIPT_DIR


echo "Installing python packages"
pip3 install -r $SCRIPT_DIR/requirements.txt --break-system-packages
