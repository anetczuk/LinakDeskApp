#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


cd $SCRIPT_DIR


sudo apt install python3-pyqt5

pip3 install -r $SCRIPT_DIR/requirements.txt

## installing package
#pip3 install -e .
