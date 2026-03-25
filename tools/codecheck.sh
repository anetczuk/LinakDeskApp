#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


## leave empty to resolve by PATH
## set variable in case of virtual environment - it will check and ensure that tool installation is added to pyproject.toml
COMMAND_PATH=""
if [ ! -z ${VIRTUAL_ENV+x} ]; then
    ## Python virtual environment detected -- use command from venv
    COMMAND_PATH="${VIRTUAL_ENV}/bin/"
fi


src_dir=$SCRIPT_DIR/../src


## E115 intend of comment
## E126 continuation line over-indented for hanging indent
## E201 whitespace after '('
## E202 whitespace before ')'
## E221 multiple spaces before equal operator
## E241 multiple spaces after ':'
## E262 inline comment should start with '# '
## E265 block comment should start with '# '
## E266 too many leading '#' for block comment
## E402 module level import not at top of file
## E501 line too long (80 > 79 characters)
## W391 blank line at end of file
## D    all docstyle checks
ignore_errors=E115,E126,E201,E202,E221,E241,E262,E265,E266,E402,E501,W391,D


"${COMMAND_PATH}"pycodestyle --show-source --statistics --count --ignore=$ignore_errors $src_dir
echo "pep8 -- no warnings found"
echo


## F401 'PyQt5.QtCore' imported but unused
ignore_errors=$ignore_errors,F401


"${COMMAND_PATH}"flake8 --show-source --statistics --count --ignore=$ignore_errors $src_dir
echo "flake8 -- no warnings found"
echo
