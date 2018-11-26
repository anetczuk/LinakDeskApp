#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"



find $SCRIPT_DIR -name "*.py" | xargs sed -i 's/[ \t]*$//'
