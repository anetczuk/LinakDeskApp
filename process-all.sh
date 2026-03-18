#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


## check installation scripts
"$SCRIPT_DIR"/tools/installvenv.sh --no-prompt

echo "running tests"
for test_runner in "$SCRIPT_DIR"/src/test*/runtests.py; do
    $test_runner 
done

# echo "running tests under venv"
# # run tests in venv (it verifies required packages)
# "$SCRIPT_DIR"/venv/runtests.py

if [ -f "$SCRIPT_DIR/examples/generate-all.sh" ]; then
    echo "generating examples results"
    "$SCRIPT_DIR"/examples/generate-all.sh --venv
fi

echo "checking code"
"$SCRIPT_DIR"/tools/checkall.sh


echo "processing completed"
