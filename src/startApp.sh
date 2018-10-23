#!/bin/bash

set -e


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


cd $SCRIPT_DIR/linakdeskapp

python3 main.py "$@"

exit_code=$?


if [ $exit_code -ne 0 ]; then
    echo "abnormal application exit: $exit_code"
fi

