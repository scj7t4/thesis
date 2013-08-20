all: report.pdf

report.pdf: report.bbl TRANS-SRC-100-GROUP.png TRANS-SRC-100-SIZE.png
	pdflatex report.tex

report.bbl: report.bib
	pdflatex report.tex
	bibtex report.aux
	pdflatex report.tex

TRANS-SRC-100-GROUP.png: TRANS-SRC-100-GROUP.gnu
	gnuplot TRANS-SRC-100-GROUP.gnu

TRANS-SRC-100-SIZE.png: TRANS-SRC-100-SIZE.gnu
	gnuplot TRANS-SRC-100-SIZE.gnu
