#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


python3 $SCRIPT_DIR/linakdeskapp/main.py "$@"

exit_code=$?


if [ $exit_code -ne 0 ]; then
    echo "abnormal application exit: $exit_code"
fi

