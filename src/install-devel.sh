#!/bin/bash

##
## Script installs package in "editable" mode (symlinks) into Python's user directory.
##

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
ROOT_DIR=$(realpath "$SCRIPT_DIR/..")


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

pip3 install --user -e "$ROOT_DIR"

if [ "${#DEV_DEPENDENCIES[@]}" -gt 0 ]; then
    pip3 install --user "${DEV_DEPENDENCIES[@]}"
fi
