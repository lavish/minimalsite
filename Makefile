# minimalsite - minimal static web site builder
# See LICENSE file for copyright and license details.

PROJECT	= minimalsite
VERSION	= 0.99
OBJ	= ${PROJECT}.pyc default_template.pyc example_template.pyc __pycache__
SRC	= ${PROJECT} default_template.py example_template.py templates/example.py style.css
DOC	= doc/

${PROJECT}:

clean:
	@echo Cleaning
	@rm -rf ${OBJ} ${PROJECT}-${VERSION}.tar.gz 

doc:
	@echo Generating documentation
	@rm -rf ${DOC}
	@mkdir ${DOC}
	@pydoc ${PROJECT} > ${DOC}${PROJECT}.txt
	@pydoc default_template > ${DOC}default_template.txt
	@pydoc example_template > ${DOC}example_template.txt

dist: clean doc
	@echo Creating dist tarball
	mkdir -p ${PROJECT}-${VERSION}
	@cp -R README.md LICENSE Makefile ${DOC} ${SRC} ${PROJECT}-${VERSION}
	@tar --exclude=".*" -cf ${PROJECT}-${VERSION}.tar ${PROJECT}-${VERSION}
	@gzip ${PROJECT}-${VERSION}.tar
	rm -rf ${PROJECT}-${VERSION}
	md5sum -b ${PROJECT}-${VERSION}.tar.gz

.PHONY: doc clean dist
