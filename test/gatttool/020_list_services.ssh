#!/bin/bash


if [ "$#" -ne 1 ]; then
    echo "illegal number of parameters -- BT mac address missing"
    exit 1
fi

btAddress="$1"


echo "Services:"
gatttool -t random -b "$btAddress" --primary

echo -e "\nCharacteristics:"
gatttool -t random -b "$btAddress" --characteristics

echo -e "\nDescriptors:"
gatttool -t random -b "$btAddress" --char-desc 
