#Specify the file to work on
SOURCE=journal2
LATEX=pdflatex
LATEX_ARGS=-halt-on-error 
BIBTEX=bibtex
VIEWER=zathura

LATEX_COMMAND=$(LATEX) $(LATEX_ARGS)
BIBTEX_COMMAND=$(BIBTEX)

all: plots $(SOURCE).pdf

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

journal: journal.tex latex_bibliography.bib
	$(LATEX_COMMAND) journal.tex
	$(BIBTEX_COMMAND) journal.aux
	$(LATEX_COMMAND) journal.tex
	$(LATEX_COMMAND) journal.tex

journal2: journal2.tex latex_bibliography.bib
	$(LATEX_COMMAND) journal2.tex
	$(BIBTEX_COMMAND) journal2.aux
	$(LATEX_COMMAND) journal2.tex
	$(LATEX_COMMAND) journal2.tex

view: all
	$(VIEWER) $(SOURCE).pdf

plots:
	make -C ./charts clean
	make -C ./charts all SIZE_X=4 SIZE_Y=3

clean:
	rm -f $(SOURCE).{aux,bbl,blg,dvi,glg,glo,gls,idx,ist,fff,nlo,nls,ilg}
	rm -f $(SOURCE).{lof,log,lot,out,toc,pdf,ps,ttt,xdy}
