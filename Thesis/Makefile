#Specify the file to work on
SOURCE=dissertation

all: base special

bibliography: $(SOURCE).aux latex_bibliography.bib
	bibtex $(SOURCE).aux 

index: $(SOURCE).idx
	makeindex $(SOURCE).idx

base: $(SOURCE).tex
	pdflatex $(SOURCE).tex

special: $(SOURCE).tex bibliography index
	pdflatex $(SOURCE).tex
	pdflatex $(SOURCE).tex

view: base special
	zathura $(SOURCE).pdf

clean:
	rm -f $(SOURCE).{aux,bbl,blg,dvi,glg,glo,gls,idx,ist,fff,nlo,nls,ilg}
	rm -f $(SOURCE).{lof,log,lot,out,toc,pdf,ps,ttt,xdy}
