# minimalsite - minimal static web site builder
# See LICENSE file for copyright and license details.

PROJECT	= minimalsite
VERSION	= 0.5
OBJ	= ${PROJECT}.pyc templates/__init__.pyc templates/default.pyc
SRC	= ${PROJECT}.py  templates/__init__.py  templates/default.py  style.css

${PROJECT}:

clean:
	@echo cleaning
	@rm -f ${OBJ} ${PROJECT}-${VERSION}.tar.gz

dist: clean
	@echo creating dist tarball
	mkdir -p ${PROJECT}-${VERSION}
	@cp -R README.md LICENSE Makefile templates ${PROJECT}.py ${PROJECT}-${VERSION}
	@tar --exclude=".*" -cf ${PROJECT}-${VERSION}.tar ${PROJECT}-${VERSION}
	@gzip ${PROJECT}-${VERSION}.tar
	rm -rf ${PROJECT}-${VERSION}
	md5sum -b ${PROJECT}-${VERSION}.tar.gz

.PHONY: clean
