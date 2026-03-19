#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
SRC_DIR="$SCRIPT_DIR/src"
VENV_DIR="$SCRIPT_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"


PYCODSTYLE_IGNORE=E115,E126,E201,E202,E221,E241,E262,E265,E266,E402,E501,W391,D
FLAKE8_IGNORE=$PYCODSTYLE_IGNORE,F401
PYDOCSTYLE_IGNORE=D100,D101,D102,D103,D104,D105,D107

echo "preparing virtual environment"
if [ ! -x "$PYTHON_BIN" ]; then
    python3 -m venv "$VENV_DIR"
fi

echo "installing dependencies"
"$PYTHON_BIN" -m pip install --upgrade pip
"$PIP_BIN" install -e ".[dev]"

echo "running tests"
for test_runner in "$SCRIPT_DIR"/src/test*/runtests.py; do
    "$PYTHON_BIN" "$test_runner"
done

# echo "running tests under venv"
# # run tests in venv (it verifies required packages)
# "$SCRIPT_DIR"/venv/runtests.py

if [ -f "$SCRIPT_DIR/examples/generate-all.sh" ]; then
    echo "generating examples results"
    "$SCRIPT_DIR"/examples/generate-all.sh --venv
fi

echo "checking code"
"$VENV_DIR/bin/pycodestyle" --show-source --statistics --count --ignore="$PYCODSTYLE_IGNORE" "$SRC_DIR"
"$VENV_DIR/bin/flake8" --show-source --statistics --count --ignore="$FLAKE8_IGNORE" "$SRC_DIR"
"$VENV_DIR/bin/pydocstyle" --count --convention=numpy --add-ignore="$PYDOCSTYLE_IGNORE" "$SRC_DIR"


echo "processing completed"
