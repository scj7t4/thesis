default: all

all: $(addsuffix .pdf, $(basename $(wildcard *.gnu) ) )

%.pdf : %.gnu
	gnuplot -e "SIZE_X=${SIZE_X};SIZE_Y=${SIZE_Y}" $*.gnu
	sed -e 's;INPUTFILE;$*.tex;' -e 'w $*.fig' -n CHART.TEMPLATE
	pdflatex $*.fig
	convert $*.pdf $*.png
	rm -f $*.{aux,bbl,blg,dvi,glg,glo,gls,idx,ist,fff,nlo,nls,ilg}
	rm -f $*.{lof,log,lot,out,toc,ps,ttt,xdy,fig,tex,tex.aux,eps}
	rm -f $*-eps-converted-to.pdf

clean:
	rm -f *.{aux,bbl,blg,dvi,glg,glo,gls,idx,ist,fff,nlo,nls,ilg}
	rm -f *.{lof,log,lot,out,toc,ps,ttt,xdy,fig,tex,tex.aux,eps}
	rm -f *-eps-converted-to.pdf
	rm -f *.pdf
