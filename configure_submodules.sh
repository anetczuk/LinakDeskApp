#!/bin/bash


git submodule init 
git submodule update --remote


git submodule foreach --recursive git checkout master
