#!/bin/bash

set -e


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


cd "$SCRIPT_DIR"/..

echo "checking links in MD files"
python3 -m mdlinkscheck -d . --implicit-heading-id-github --excludes ".*/tmp/.*" ".*/src/test.*/.*" ".*/venv/.*"
