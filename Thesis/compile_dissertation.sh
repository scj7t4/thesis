#!/bin/bash

#texfile="dissertation_publication"
texfile="dissertation"
#texfile="ptotemplate"

rm -f $texfile.{aux,bbl,blg,dvi,glg,glo,gls,idx,ist,fff,nlo,nls,ilg}
rm -f $texfile.{lof,log,lot,out,toc,pdf,ps,ttt,xdy}

#makeindx $texfile.idx && \
pdflatex $texfile.tex && \
bibtex $texfile.aux && \
pdflatex $texfile.tex && \
pdflatex $texfile.tex

#  this chokes on big dvi
#dvipdf $texfile

#  create ps from dvi. Works for large files
#dvips $texfile.dvi


#  ps2pdf chokes on big files
#ps2pdf $texfile.ps 

#pdflatex $texfile.tex


#evince $texfile.ps
zathura $texfile.pdf
