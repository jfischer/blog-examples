SHELL=/bin/bash

ROOT_PATH=$(shell cd ~; pwd)

all: ml_walker go_walker JavaWalker.class

ml_walker: ml_walker.ml
	ocamlopt -o ml_walker unix.cmxa ml_walker.ml

go_walker: go_walker.go
	go build go_walker.go

JavaWalker.class: JavaWalker.java
	javac JavaWalker.java

run: all
	echo "Root path is $(ROOT_PATH)"
	time java JavaWalker $(ROOT_PATH)
	time ./go_walker $(ROOT_PATH)
	time ./ml_walker $(ROOT_PATH)
	time python py_walker.py $(ROOT_PATH)

clean:
	rm -f *~ ml_walker *.cmo *.cmx *.cmi *.o *.pyc go_walker \
	      *.class


.PHONY: clean all run
