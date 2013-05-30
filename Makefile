SHELL=/bin/bash
HTMLDIR=doc/build/html
HTMLSED=find ${HTMLDIR}/ -name '*.html' | xargs sed -i

.PHONY: usage install deps test doc gh-pages build-doc

usage:
	@echo
	@echo Makefile for yajl-py
	@echo
	@echo Targets
	@echo " install :" easy_install yajl-py
	@echo " deps    :" install compatible yajl version
	@echo " test    :" run yajl-py tests 
	@echo " doc     :" install docs to gh-pages branch

install:
	pip install . --use-mirrors

test:
	pip install -r test_requirements.txt --use-mirrors
	nosetests -v tests/ --with-coverage --cover-inclusive --cover-package yajl

doc: gh-pages

gh-pages: build-doc
	git co gh-pages
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
	(cd yajl-src; git checkout 4c539cb5b; git reset --hard; ./configure)
	sudo make -C yajl-src install
	sudo ldconfig
