#!/bin/bash

PACKAGES_DIR=packages


shopt -s nullglob # Prevent f from being "*.tex"
cd $1
# Given an input directory, generate a file that inputs all the others.
echo "% This file is auto-generated, do not edit" > $2/__packages.generated
for f in *.tex; do
	echo $f
	echo "\input{${PACKAGES_DIR}/$f}" >> $2/__packages.generated
done
