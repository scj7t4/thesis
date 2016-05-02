default: all

all: document

document:
	rm -f build/packages/__packages.generated
	mkdir -p build
	cd build; \
	cmake ../src; \
	make
	cp build/main.pdf dissertation.pdf
