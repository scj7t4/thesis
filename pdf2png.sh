#!/bin/bash

shopt -s nullglob
for f in $1/*.pdf
do
    echo "Processing $f file..."
    fpath=$(dirname $f)
    bname=$(basename $f)
    fileext=${f##*.}
    fname=${bname%.*}
    convert -density 300 $f -quality 100 $2/$fname.png
done
