#!/bin/bash


git submodule init 
git submodule update


git submodule foreach --recursive git checkout master
