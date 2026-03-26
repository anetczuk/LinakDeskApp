#!/bin/bash

##
## Run all tests and code check tool.
## Pass --release to use fresh venv installation.
##

set -eu


SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

VENV_DIR="$SCRIPT_DIR/.venv"


ARGS=()
RELEASE_RUN=false

while :; do
    if [ -z "${1+x}" ]; then
        ## end of arguments (prevents unbound argument error)
        break
    fi

    case "$1" in
      -r|--release)      RELEASE_RUN=true 
                         shift ;;

      *)  ARGS+=("$1")
          shift ;;
    esac
done


ACTIVATE_VENV_PATH="$VENV_DIR/activatevenv.sh"


if [ "$RELEASE_RUN" = false ]; then
    PYTHON_BIN="$VENV_DIR/bin/python"
    if [ ! -x "$PYTHON_BIN" ]; then
        ## install venv
        echo "Preparing virtual environment"
        "$SCRIPT_DIR"/tools/installvenv.sh --dev --no-prompt
    else
        echo "Skipping venv installation"
        echo
    fi
else
    VENV_NAME=".venv_release"

    "$SCRIPT_DIR"/tools/installvenv.sh --no-prompt "../${VENV_NAME}"

    VENV_DIR="$SCRIPT_DIR/${VENV_NAME}"
    ACTIVATE_VENV_PATH="$VENV_DIR/activatevenv.sh"

    ## install development tools (e.g. for static code checks)
    $ACTIVATE_VENV_PATH "${SCRIPT_DIR}/src/install-deps.sh --dev"
fi


echo "generating docs"
"$SCRIPT_DIR"/doc/generate-doc.sh


# run tests in venv (it verifies required packages)
echo
echo "Running tests"
"$VENV_DIR"/runtests.py


if [ -f "$SCRIPT_DIR/examples/generate-all.sh" ]; then
    echo "generating examples results"
    "$SCRIPT_DIR"/examples/generate-all.sh --venv
fi


echo
echo
echo "Checking code"
$ACTIVATE_VENV_PATH "$SCRIPT_DIR/tools/checkall.sh"


echo
echo "Processing completed"
