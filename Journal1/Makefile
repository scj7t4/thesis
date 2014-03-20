#Specify the file to work on
SOURCE=journal

all: plots $(SOURCE).pdf

bibliography: base $(SOURCE).aux latex_bibliography.bib
	bibtex $(SOURCE).aux 

#index: base $(SOURCE).idx
#	makeindex $(SOURCE).idx

base: $(SOURCE).tex
	pdflatex $(SOURCE).tex

$(SOURCE).pdf: bibliography 
    #index
	pdflatex $(SOURCE).tex
	pdflatex $(SOURCE).tex

view: all
	zathura $(SOURCE).pdf

plots:
	make -C ./gnuplots all

clean:
	rm -f $(SOURCE).{aux,bbl,blg,dvi,glg,glo,gls,idx,ist,fff,nlo,nls,ilg}
	rm -f $(SOURCE).{lof,log,lot,out,toc,pdf,ps,ttt,xdy}
