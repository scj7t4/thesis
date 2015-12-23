#Specify the file to work on
SOURCE=editing
LATEX=pdflatex
LATEX_ARGS=-halt-on-error 
BIBTEX=bibtex
VIEWER=zathura

LATEX_COMMAND=$(LATEX) $(LATEX_ARGS)
BIBTEX_COMMAND=$(BIBTEX)

all: $(SOURCE).pdf

bibliography: base $(SOURCE).aux latex_bibliography.bib
	$(BIBTEX_COMMAND) $(SOURCE).aux 

#index: base $(SOURCE).idx
#	makeindex $(SOURCE).idx

base: $(SOURCE).tex
	$(LATEX_COMMAND) $(SOURCE).tex

$(SOURCE).pdf: bibliography 
    #index
	$(LATEX_COMMAND) $(SOURCE).tex
	$(LATEX_COMMAND) $(SOURCE).tex

editing: editing.tex latex_bibliography.bib
	$(LATEX_COMMAND) editing.tex
	$(BIBTEX_COMMAND) editing.aux
	$(LATEX_COMMAND) editing.tex
	$(LATEX_COMMAND) editing.tex

conference: conference.tex latex_bibliography.bib
	$(LATEX_COMMAND) conference.tex
	$(BIBTEX_COMMAND) conference.aux
	$(LATEX_COMMAND) conference.tex
	$(LATEX_COMMAND) conference.tex

view: all
	$(VIEWER) $(SOURCE).pdf

clean:
	rm -f $(SOURCE).{aux,bbl,blg,dvi,glg,glo,gls,idx,ist,fff,nlo,nls,ilg}
	rm -f $(SOURCE).{lof,log,lot,out,toc,pdf,ps,ttt,xdy}
