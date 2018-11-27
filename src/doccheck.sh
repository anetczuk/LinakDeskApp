#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


src_dir=$SCRIPT_DIR


## D100: Missing docstring in public module
## D101: Missing docstring in public class
## D102: Missing docstring in public method
## D103: Missing docstring in public function
## D104: Missing docstring in public package
## D107 Missing docstring in __init__
ignore_errors=D100,D101,D102,D103,D104,D107


# pydocstyle --count --ignore=$ignore_errors $src_dir
pydocstyle --count --convention=numpy --add-ignore=$ignore_errors $src_dir
exit_code=$?

if [ $exit_code -ne 0 ]; then
    exit $exit_code
fi

echo "docstyle -- no warnings found"
