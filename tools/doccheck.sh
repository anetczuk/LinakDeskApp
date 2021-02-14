#!/bin/bash


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


src_dir=$SCRIPT_DIR/../src


## D100: Missing docstring in public module
## D101: Missing docstring in public class
## D102: Missing docstring in public method
## D103: Missing docstring in public function
## D104: Missing docstring in public package
## D105: Missing docstring in magic method
## D107 Missing docstring in __init__
ignore_errors=D100,D101,D102,D103,D104,D105,D107


# pydocstyle --count --ignore=$ignore_errors $src_dir
pydocstyle --count --convention=numpy --add-ignore=$ignore_errors $src_dir
exit_code=$?

if [ $exit_code -ne 0 ]; then
    exit $exit_code
fi

echo "docstyle -- no warnings found"
