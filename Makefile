# minimalsite - minimal static web site builder
# See LICENSE file for copyright and license details.

PROJECT	= minimalsite
VERSION	= 0.91
OBJ	= ${PROJECT}.pyc templates/__init__.pyc templates/default.pyc templates/example.pyc __pycache__ templates/__pycache__
SRC	= ${PROJECT}  templates/__init__.py  templates/default.py  templates/example.py style.css
DOC	= doc/

${PROJECT}:

clean:
	@echo Cleaning
	@rm -rf ${OBJ} ${PROJECT}-${VERSION}.tar.gz 

doc:
	@echo Generating documentation
	@rm -rf ${DOC}
	@mkdir ${DOC}
	@pydoc minimalsite > ${DOC}minimalsite.txt
	@pydoc templates > ${DOC}templates.txt
	@pydoc templates.default > ${DOC}templates.default.txt
	@pydoc templates.example > ${DOC}templates.example.txt

dist: clean doc
	@echo Creating dist tarball
	mkdir -p ${PROJECT}-${VERSION}
	@cp -R README.md LICENSE Makefile templates doc ${PROJECT}.py style.css ${PROJECT}-${VERSION}
	@tar --exclude=".*" -cf ${PROJECT}-${VERSION}.tar ${PROJECT}-${VERSION}
	@gzip ${PROJECT}-${VERSION}.tar
	rm -rf ${PROJECT}-${VERSION}
	md5sum -b ${PROJECT}-${VERSION}.tar.gz

.PHONY: doc clean dist
