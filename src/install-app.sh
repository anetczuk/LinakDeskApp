#!/bin/bash

##
## Script installs application (copy of package) into Python's user directory.
## When --dev flag given then install in "editable" mode (symlinks).
##

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
ROOT_DIR=$(realpath "$SCRIPT_DIR/..")


ARGS=()
SYSTEM_MODE=false
DEV_MODE=false

while :; do
    if [ -z "${1+x}" ]; then
        ## end of arguments (prevents unbound argument error)
        break
    fi

    case "$1" in
      --system-mode)   SYSTEM_MODE=true 
                       shift ;;
      --dev)        DEV_MODE=true 
                    shift ;;
      *)  ARGS+=("$1")
          shift ;;
    esac
done


if [ ! -z ${VIRTUAL_ENV+x} ]; then
    ## Python virtual environment detected -- installing to system directory
    SYSTEM_MODE=true
fi


PIP_ARGS=""

if [ "$SYSTEM_MODE" = false ]; then
    echo "Installing application into user directory"
    echo

    PIP_ARGS="--user"
else
    echo "Installing application into system directory"
    echo
fi



cd "$ROOT_DIR"

if [ "$DEV_MODE" = false ]; then
    ##
    ## install in standard mode
    ##

    python3 -m pip install "$PIP_ARGS" '.'

else
    ##
    ## install in development mode 
    ##

    echo "Installing application in developer mode"
    echo

    python3 -m pip install "$PIP_ARGS" -e '.[dev]'
fi


echo
echo "Installation done"
echo
