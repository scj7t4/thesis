#!/bin/bash

for f in *.pdf
do
    filename="${f%.*}"
    convert ${filename}.pdf pngs/${filename}.png
done
