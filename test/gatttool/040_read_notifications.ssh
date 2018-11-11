#!/bin/bash


if [ "$#" -ne 1 ]; then
    echo "illegal number of parameters -- BT mac address missing"
    exit 1
fi

btAddress="$1"


echo -e "\nNotifications status:"
gatttool -t random -b "$btAddress" --char-read -u 0x2902

