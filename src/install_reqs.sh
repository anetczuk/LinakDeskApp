#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


cd $SCRIPT_DIR


echo "Installing system package" 
sudo apt install python3-pyqt5

echo "Installing python packages"
pip3 install -r $SCRIPT_DIR/requirements.txt
