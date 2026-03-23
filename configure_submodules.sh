#!/bin/bash

##
## Configure submodules. Use for submodules development.
##

git submodule init 
git submodule update --remote


git submodule foreach --recursive git checkout master
