#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


src_dir=$SCRIPT_DIR


## E115 intend of comment
## E126 continuation line over-indented for hanging indent
## E201 whitespace after '('
## E202 whitespace before ')'
## E221 multiple spaces before equal operator
## E262 inline comment should start with '# '
## E265 block comment should start with '# '
## E266 too many leading '#' for block comment
## E402 module level import not at top of file
## E501 line too long (80 > 79 characters)
## W391 blank line at end of file
ignore_errors=E115,E126,E201,E202,E221,E262,E265,E266,E402,E501,W391


pycodestyle --show-source --statistics --count --ignore=$ignore_errors $src_dir
exit_code=$?

if [ $exit_code -ne 0 ]; then
    exit $exit_code
fi

echo "pep8 -- no warnings found"


## F401 'PyQt5.QtCore' imported but unused
ignore_errors=$ignore_errors,F401


flake8 --show-source --statistics --count --ignore=$ignore_errors $src_dir

