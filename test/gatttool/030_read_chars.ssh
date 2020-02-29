#!/bin/bash

set -eu


if [ "$#" -ne 1 ]; then
    echo "illegal number of parameters -- BT mac address missing"
    exit 1
fi

btAddress="$1"


## $1 -- input
convertToString() {
    local gattValue=$1
    local hexValue=$(awk -F: '{print $2}' <<< "$gattValue")
    local hexValue=${hexValue// /}
    local stringValue=$(echo $hexValue | xxd -r -p)
    echo $stringValue
}


echo -e "Device name:"
gattValue=$(gatttool -t random -b "$btAddress" --char-read -a 0x0003)
stringValue=$(convertToString "$gattValue")
echo "$gattValue, string: $stringValue"

echo -e "\nManufacturer:"
gattValue=$(gatttool -t random -b "$btAddress" --char-read -a 0x0018)
stringValue=$(convertToString "$gattValue")
echo "$gattValue, string: $stringValue"

echo -e "\nVersion:"
gatttool -t random -b "$btAddress" --char-read -a 0x0019

echo -e "\nModel Number:"
gattValue=$(gatttool -t random -b "$btAddress" --char-read -a 0x001a)
stringValue=$(convertToString "$gattValue")
echo "$gattValue, string: $stringValue"

echo -e "\nHeight and speed:"
gatttool -t random -b "$btAddress" --sec-level=medium --char-read -a 0x001d
