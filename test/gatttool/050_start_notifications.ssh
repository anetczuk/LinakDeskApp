#!/bin/bash


if [ "$#" -ne 1 ]; then
    echo "illegal number of parameters -- BT mac address missing"
    exit 1
fi

btAddress="$1"


echo -e "\nNotifications status:"
gatttool -t random -b "$btAddress" --char-read -u 0x2902

## service changed
gatttool -t random -b "$btAddress" --char-write-req -a 0x0b -n 0x01
## error
gatttool -t random -b "$btAddress" --sec-level=medium --char-write-req -a 0x11 -n 0x01
## DPG
gatttool -t random -b "$btAddress" --char-write-req -a 0x15 -n 0x01
## height and speed
gatttool -t random -b "$btAddress" --sec-level=medium --char-write-req -a 0x1e -n 0x01
## TWO
gatttool -t random -b "$btAddress" --char-write-req -a 0x21 -n 0x01

echo -e "\nNotifications status:"
gatttool -t random -b "$btAddress" --char-read -u 0x2902

