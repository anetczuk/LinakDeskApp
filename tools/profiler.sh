#!/bin/bash

set -eu


##
## usage example: ./tool/profiler.sh --cprofile <Python-script> <Python-script-args>
##


ARGS=()
PROFILER=""

while :; do
    if [ -z "${1+x}" ]; then
        ## end of arguments (prevents unbound argument error)
        break
    fi

    case "$1" in
      --cprofile)   PROFILER="cprofile" 
                    shift ;;

      --mtprof)     PROFILER="mtprof" 
                    shift ;;

      --viztracer)  PROFILER="viztracer" 
                    shift ;;

      *)  ARGS+=("$1")
          shift ;;
    esac
done


if [ "$PROFILER" == "cprofile" ]; then
    tmpdir=$(dirname "$(mktemp -u)")
    timestamp=$(date +%s)

    out_file=$(mktemp "${tmpdir}/out.${timestamp}.XXXXXX.prof")
    #out_file="$(pwd)/out.prof"

    echo "Starting cprofile"
    echo "executing: python3 -m cProfile -o $out_file ${ARGS[@]}"

    python3 -m cProfile -o "$out_file" "${ARGS[@]}"

    echo ""
    echo "View output: pyprof2calltree -k -i $out_file"

    ### browser based, installation: pip3 install snakeviz
    echo "Borowser-based view output: snakeviz $out_file"
    
    exit 0
fi


if [ "$PROFILER" == "mtprof" ]; then
    tmpdir=$(dirname "$(mktemp -u)")
    timestamp=$(date +%s)

    out_file=$(mktemp "${tmpdir}/out.${timestamp}.XXXXXX.prof")
    #out_file="$(pwd)/out.prof"

    echo "Starting mtprof"
    echo "executing: python3 -m mtprof -o $out_file ${ARGS[@]}"

    python3 -m mtprof -o "$out_file" "${ARGS[@]}"

    echo ""
    echo "View output: pyprof2calltree -k -i $out_file"

    ### browser based, installation: pip3 install snakeviz
    echo "Borowser-based view output: snakeviz $out_file"
    
    exit 0
fi


if [ "$PROFILER" == "viztracer" ]; then
    tmpdir=$(dirname "$(mktemp -u)")
    timestamp=$(date +%s)

    out_file=$(mktemp "${tmpdir}/report.${timestamp}.XXXXXX.json")
    #out_file="$(pwd)/out.prof"

    echo "Starting viztracer"
    echo "executing: viztracer -o $out_file ${ARGS[@]}"

    viztracer -o "$out_file" -- "${ARGS[@]}"

    exit 0
fi


echo "no profiler selected, pass: --cprofile or --mtprof or --viztracer"
exit 1
