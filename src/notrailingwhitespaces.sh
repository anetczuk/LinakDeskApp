#!/bin/bash


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")



find $SCRIPT_DIR -name "*.py" | xargs sed -i 's/[ \t]*$//'
