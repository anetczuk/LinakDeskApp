#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


ENV_DIR=$SCRIPT_DIR/../venv


if [ -d "$ENV_DIR" ]; then
    echo "Given target directory [$ENV_DIR] exists, remove it and restart the script"
    exit 1
fi
    

echo "Creating virtual environment in $ENV_DIR"

python3 -m venv $ENV_DIR
