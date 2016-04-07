SHELL=/bin/bash
HTMLDIR=doc/build/html
HTMLSED=find ${HTMLDIR}/ -name '*.html' | xargs sed -i ''

.PHONY: usage install deps test doc gh-pages build-doc

usage:
	@echo
	@echo Makefile for yajl-py
	@echo
	@echo Targets
	@echo " install :" pip install yajl-py
	@echo " deps    :" install compatible yajl version
	@echo " test    :" run yajl-py tests 
	@echo " doc     :" install docs to gh-pages branch

install:
	pip install .

test:
	pip install -r test_requirements.txt
	nosetests --with-cov --cover-erase --cov yajl -v tests/

doc: gh-pages

gh-pages: build-doc
	git checkout gh-pages
	rsync -vcr ${HTMLDIR}/ ./

build-doc:
	make -C doc/ clean html
	mv ${HTMLDIR}/{_,}sources
	${HTMLSED} 's/_sources/sources/g'
	mv ${HTMLDIR}/{_,}static
	${HTMLSED} 's/_static/static/g'

deps:
	rm -fr yajl-src
	git clone https://github.com/lloyd/yajl.git yajl-src
	(cd yajl-src; git checkout 12ee82ae51; git reset --hard; ./configure)
	sudo make -C yajl-src install
	sudo ldconfig
