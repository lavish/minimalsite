MinimalSite
===========

A fast minimal static website builder.

Minimalsite generates web pages from a source file hierarchy. It supports
markdown and textile syntax, but plain txt and html can be evenly used.
Template files are python modules, providing huge flexibilty and keeping the
codebase tiny and simple.


### Requirements

In order to run minimalsite you need a working Python 2.X or 3.X installation.
If you plan to yse markdown or textile syntax, one of the following modules is
required:

* [Python Markdown][] for markdown syntax support
* [PyTextile][] for textile syntax support


### Installation

There's no need to install the tool: download, unpack and run.


### Running minimalsite

	usage: minimalsite.py [-h] -t TEMPLATE [-V] [-s SRC] [-d DST] [-v]
	
	Fast minimal static website builder
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -t TEMPLATE, --template TEMPLATE
	                        specify a template file name. Valid templates must
	                        terminate with '_template.py'
	  -V, --verbose         verbosely display site structure
	  -s SRC, --src SRC     source dir, where the textual hierarchy resides
	  -d DST, --dst DST     destination dir, where the html pages will be written
	  -v, --version         show program's version number and exit

You must start minimalsite providing a valid template file.

Please note that you need to place an index file in each directory you want to
parse. Those directories will be ignored otherwise.


### Configuration

You can create your own template starting from `default_template.py`. See
comments inside for help. Templates provide a very flexible tool for building
your site by adding how many functions and features you want; See
`example_template.py` for a more advanced template.


### Features

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


### Example

The following example explains how to run minimalsite to create a simple site
using the default template. Source markdown files are written under
`/home/lavish/mysite`, while the site is generated under `/var/www/htdocs/`.

	$ mkdir /home/lavish/mysite
	$ cd /home/lavish/mysite
	$ echo "Hi all" > index.md
	$ echo "List of my publications" > publications.md
	$ echo "You can send me a postcard here..." > contacts.md
	$ mkdir software
	$ echo "I contributed to the following projects..." > software/index.md
	$ echo "A great editor" > software/vim.md
	$ echo "A great mail client" > software/mutt.md
	$ echo "A great irc client" > software/irssi.md
	$ minimalsite.py -s /home/lavish/mysite -d /var/www/htdocs \
	                 -t /usr/local/share/minimalsite/default_template.py
	[*] Processing files from /home/lavish/mysite
	[*] Writing html files into /var/www/htdocs
	    /var/www/htdocs/contacts.html
	    /var/www/htdocs/index.html
	    /var/www/htdocs/software
		/var/www/htdocs/software/irssi.html
		/var/www/htdocs/software/index.html
		/var/www/htdocs/software/vim.html
		/var/www/htdocs/software/mutt.html
	    /var/www/htdocs/publications.html
	$


### Misc

Please refear to [Markdown Syntax][] and [Textile Syntax][] documentation before writing your pages.


### Author/Credits

Minimalsite is written by [Marco Squarcina][] <lavish@gmail.com>

The following people have contributed to this project:

* [Anselm R Garbe][], provided the idea behind this tool (genosite)
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
[Luca Postregna]:     http://luca.postregna.name/
[Emanuele Giaquinta]: http://tomaw.net/~exg/
