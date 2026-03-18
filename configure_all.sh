#!/bin/bash


set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

SRC_DIR=$SCRIPT_DIR/src


echo "Installing dependencies"
$SRC_DIR/install-deps.sh --break-system-packages

echo "Configuring bluepy"
$SRC_DIR/configure_bluepy.sh

echo "Configuring submodules"
$SCRIPT_DIR/configure_submodules.sh
