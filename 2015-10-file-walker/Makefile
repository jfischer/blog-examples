SHELL=/bin/bash

ROOT_PATH=$(shell cd ~; pwd)

all: ml_walker go_walker JavaWalker.class

ml_walker: ml_walker.ml check_ocaml_deps
	ocamlopt -o ml_walker -I `ocamlfind query fileutils` unix.cmxa fileutils-str.cmxa fileutils.cmxa ml_walker.ml

go_walker: go_walker.go
	go build go_walker.go

JavaWalker.class: JavaWalker.java
	javac JavaWalker.java

test: all
	echo "Root path is $(ROOT_PATH)"
	java JavaWalker $(ROOT_PATH)
	./go_walker $(ROOT_PATH)
	./ml_walker $(ROOT_PATH)
	python py_walker.py $(ROOT_PATH)

check_ocaml_deps:
	@echo "checking OCaml dependencies..."
	@if [[ `which ocamlopt` == '' ]]; then echo "Missing ocamlopt, install apt package 'ocaml'"; exit 1; fi
	@if [[ `which ocamlfind` == '' ]]; then echo "Missing ocamlfind, install apt package 'ocaml-findlib'"; exit 1; fi
	@if [[ `ocamlfind query fileutils` == '' ]]; then echo "Missing fileutils, need to install it manually - see README.rst for details"; exit 1; fi

	@echo "dependency check successful."

clean:
	rm -f *~ ml_walker *.cmo *.cmx *.cmi *.o *.pyc go_walker \
	      *.class


.PHONY: clean all test check_ocaml_deps
