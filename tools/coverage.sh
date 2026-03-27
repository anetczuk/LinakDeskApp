#!/bin/bash

set -eu


##
## usage example: ./tool/coverage.sh <Python-script> <Python-script-args>
##


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SOURCE_DIR="$SCRIPT_DIR/../src"


timestamp=$(date +%s)
tmpdir=$(dirname "$(mktemp -u)")

htmlcov_dir="$tmpdir/htmlcov.${timestamp}"
mkdir -p "$htmlcov_dir"


#coverage_file=$(mktemp ${tmpdir}/revcrc.coverage.${timestamp}.XXXXXX)


echo "Starting coverage"


# creates .coverage in working directory - workaround is to set env variable
export COVERAGE_FILE=/tmp/.coverage

coverage run --source "$SOURCE_DIR" --omit "*/site-packages/*,*/test*/*" --branch "$@"

# coverage report
coverage html -d "$htmlcov_dir"


echo ""
echo "Coverage HTML output: file://$htmlcov_dir/index.html"


## rm ${coverage_file}
