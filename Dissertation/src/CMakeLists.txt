cmake_minimum_required( VERSION 2.6 )

project( Dissertation NONE )

include(../UseLATEX.cmake)

latex_get_output_path(output_dir)

add_latex_document(main.tex
	INPUTS
		structure/*.tex
		optional/*.tex
		chapters/*.tex
		info/*.tex
		packages/*.tex
		extras/*.tex
		contents.tex
	BIBFILES
		bibliography.bib
	IMAGE_DIRS
		media/drawings
		media/charts
	DEPENDS
		packages/__packages.generated
	FORCE_PDF
)
	
add_custom_command(OUTPUT ${output_dir}/packages/__packages.generated
	COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/../helpers/packages.sh
	ARGS ${CMAKE_CURRENT_SOURCE_DIR}/packages ${output_dir}/packages
)

