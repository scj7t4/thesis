cmake_minimum_required( VERSION 2.6 )

project( Dissertation NONE )

include(UseLATEX.cmake)

add_latex_document(main.tex
	INPUTS
		structure/*.tex
		optional/*.tex
		chapters/*.tex
		info/*.tex
		packages/*.tex
		contents.tex
	FORCE_PDF
)
	
