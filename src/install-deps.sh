#!/bin/bash

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
ROOT_DIR=$(realpath "$SCRIPT_DIR/..")


### required for pygraphviz
#sudo apt install graphviz-dev


# ## ensure required version of pip3
# pip3 install --upgrade 'pip>=18.0'


## install requirements
PIP_ARGS=""
if [[ $* == *--break-system-packages* ]]; then
    PIP_ARGS="--break-system-packages"
fi

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

pip3 install $PIP_ARGS "${DEPENDENCIES[@]}"


echo
echo "installation done"
echo
