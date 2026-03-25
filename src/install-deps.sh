#!/bin/bash

set -eu

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

PIP_ARGS=()
if [ "$SYSTEM_MODE" = false ]; then
    PIP_ARGS+=("--user")
fi


## install requirements
if [[ $* == *--break-system-packages* ]]; then
    PIP_ARGS+=("--break-system-packages")
fi


if [ "$DEV_MODE" = false ]; then
    ##
    ## install app dependencies
    ##

    mapfile -t DEPENDENCIES < <(
        python3 - "$ROOT_DIR/pyproject.toml" <<'PY'
from pathlib import Path
import sys
import tomllib

pyproject_path = Path(sys.argv[1])
project_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
for dependency in project_data.get("project", {}).get("dependencies", []):
    print(dependency)
PY
)

    if [ "${#DEPENDENCIES[@]}" -eq 0 ]; then
        echo "No dependencies declared in $ROOT_DIR/pyproject.toml"
        exit 0
    fi
    
    pip3 install ${PIP_ARGS[@]} "${DEPENDENCIES[@]}"

else
    ##
    ## install development dependencies 
    ##

    echo "Installing project dependencies with developer dependencies"
    echo

    mapfile -t DEV_DEPENDENCIES < <(
        python3 - "$ROOT_DIR/pyproject.toml" <<'PY'
from pathlib import Path
import sys
import tomllib

pyproject_path = Path(sys.argv[1])
project_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
for dependency in project_data.get("project", {}).get("optional-dependencies", {}).get("dev", []):
    print(dependency)
PY
)
    
    if [ "${#DEV_DEPENDENCIES[@]}" -eq 0 ]; then
        echo "No dependencies declared in $ROOT_DIR/pyproject.toml"
        exit 0
    fi

    pip3 install ${PIP_ARGS[@]} "${DEV_DEPENDENCIES[@]}"

fi


echo
echo "Dependencies installation done"
echo
