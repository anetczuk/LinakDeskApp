#!/bin/bash


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


src_dir=$SCRIPT_DIR/../src


find $src_dir -name "*.py" | xargs sed -i 's/[ \t]*$//'
