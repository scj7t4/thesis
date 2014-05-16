#Specify the file to work on
SOURCE=dissertation

all: plots $(SOURCE).pdf

bibliography: base $(SOURCE).aux latex_bibliography.bib
	bibtex $(SOURCE).aux 

index: base $(SOURCE).idx
	makeindex $(SOURCE).idx

base: $(SOURCE).tex
	pdflatex $(SOURCE).tex

$(SOURCE).pdf: bibliography index
	pdflatex $(SOURCE).tex
	pdflatex $(SOURCE).tex

view: all
	zathura $(SOURCE).pdf

plots:
	make -C ./gnuplots clean
	make -C ./gnuplots all SIZE_X=3.125 SIZE_Y=2.69

clean:
	rm -f $(SOURCE).{aux,bbl,blg,dvi,glg,glo,gls,idx,ist,fff,nlo,nls,ilg}
	rm -f $(SOURCE).{lof,log,lot,out,toc,pdf,ps,ttt,xdy}
