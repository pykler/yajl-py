usage:
	@echo
	@echo Makefile for yajl-py
	@echo
	@echo Targets
	@echo " install :" easy_install yajl-py
	@echo " test    :" run yajl-py tests 

install:
	easy_install .

test:
	nosetests -v tests/
