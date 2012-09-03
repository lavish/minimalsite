MinimalSite
===========

A fast minimal static website builder.

Minimalsite generates web pages from a source file hierarchy. It supports
markdown and textile syntax, but plain txt and html can be evenly used.
Templates are python modules, providing huge flexibilty and keeping the
codebase tiny and simple.


### Requirements

In order to run minimalsite you need a working Python 2.X or 3.X installation
and the following modules:

* [Python Markdown][] for markdown syntax support
* [PyTextile][] for textile syntax support


### Installation

There's no need to install the tool: download, unpack and run.


### Running minimalsite

	usage: minimalsite [-h] [-V] [-t TEMPLATE] [-s SRC] [-d DST] [-v]

	Fast minimal static website builder

	optional arguments:
	  -h, --help            show this help message and exit
	  -V, --verbose         verbosely display site structure
	  -t TEMPLATE, --template TEMPLATE
	                        specify a template: valid arguments are module names
	                        without path and extension
	  -s SRC, --src SRC     source dir, where the markdown/textile hierarchy
	                        resides
	  -d DST, --dst DST     destination dir, where the html pages will be written
	  -v, --version         show program's version number and exit

You can add your own templates under the `templates/` directory. You can feed
minimalsite with your template be specifying only the template file name, i.e.,
to use `templates/minimalblue.py`, you will run `./minimalsite -t minimalblue`

Please note that you need to place an index file in each directory you want to
parse, otherwise those directories will be ignored.


### Configuration

You can create your own template starting from `templates/default.py`. See
comments inside for help. Templates provide a very flexible tool for building
your site adding how many functions and features you want; See
`templates/example.py` for a more advanced template.


### Extra Features

#### Page ordering

If you need to order menu entries, add a numerical index before the pathname,
for example:

	/home/marco/website/30_university.md
	/home/marco/website/50_contacts.md

will be written as:

	/var/www/marco/htdocs/university.html
	/var/www/marco/htdocs/contacts.html

and "university" will be displayed before "contacts" in the menu. Both files and
directories are supported.


### Misc

Please refear to [Markdown Syntax][] and [Textile Syntax][] documentation before writing your pages.


### Author/Credits

Minimalsite is written by [Marco Squarcina][] <lavish@gmail.com>

The following people have contributed to this project:

* [Anselm R Garbe][], provided the idea behind this tool ([genosite][])
* [Luca Postregna][], testing and lots of useful suggestions
* Josie Panzuto, linguistic revision
* [Emanuele Giaquinta][], some tips


### Website

* http://www.minimalblue.com/projects/minimalsite.html
* https://github.com/lavish/minimalsite


[Python Markdown]:    http://www.freewisdom.org/projects/python-markdown
[PyTextile]:          http://loopcore.com/python-textile/
[Markdown Syntax]:    http://daringfireball.net/projects/markdown/syntax
[Textile Syntax]:     http://en.wikipedia.org/wiki/Textile_(markup_language)
[Marco Squarcina]:    http://www.minimalblue.com/
[Anselm R Garbe]:     http://garbe.us/
[genosite]:           http://hg.suckless.org/genosite/
[Luca Postregna]:     http://luca.postregna.name/
[Emanuele Giaquinta]: http://tomaw.net/~exg/
