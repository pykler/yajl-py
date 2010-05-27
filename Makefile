SHELL=/bin/bash
HTMLDIR=doc/build/html
HTMLSED=find ${HTMLDIR}/ -name '*.html' | xargs sed -i

.PHONY: usage install test doc gh-pages build-doc

usage:
	@echo
	@echo Makefile for yajl-py
	@echo
	@echo Targets
	@echo " install :" easy_install yajl-py
	@echo " test    :" run yajl-py tests 
	@echo " doc     :" install docs to gh-pages branch

install:
	easy_install .

test:
	nosetests -v tests/

doc: gh-pages

gh-pages: build-doc
	git co gh-pages
	rsync -vr ${HTMLDIR}/ ./

build-doc:
	make -C doc/ clean html
	mv ${HTMLDIR}/{_,}sources
	${HTMLSED} 's/_sources/sources/g'
	mv ${HTMLDIR}/{_,}static
	${HTMLSED} 's/_static/static/g'
