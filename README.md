MinimalSite
===========

minimalsite is a fast minimal static website builder. It generates web pages
from a file hierarchy with markdown and textile syntax.

                                               _                
               o          o                   | |     o         
     _  _  _       _  _       _  _  _    __,  | |  ,    _|_  _  
    / |/ |/ |  |  / |/ |  |  / |/ |/ |  /  |  |/  / \_|  |  |/  
      |  |  |_/|_/  |  |_/|_/  |  |  |_/\_/|_/|__/ \/ |_/|_/|__/



### Requirements

In order to run minimalsite you need a working Python 2.X installation and the
following modules:

* [Python Markdown][] for markdown syntax support
* [PyTextile][] for textile syntax support


### Installation

There's no need to install the tool: download, unpack and run.


### Running minimalsite

    Usage: minimalsite.py [options]

    Options:
      -h, --help                     Show help options
      -v, --version                  Display minimalsite version
      -t, --template=TEMPLATE        Specify a template
      -s, --src_dir=SOURCE_DIR       Specify source dir to use
      -d, --dst_dir=DESTINATION_DIR  Specify destionation dir to use

`SOURCE_DIR` is the directory containing the source file hierarchy and
`DESTINATION_DIR` the directory where you want to create web pages.

You can also add different templates under the `templates/` directory and
specify `TEMPLATE` using your template file name. For example, to use
`templates/minimalblue.py`, you will run `./minimalsite -t minimalblue ...`

Please note that you need to place an index file in in each directory you want
to parse, otherwise those directories will be ignored.


### Configuration

You can create you own template starting from `templates/default.py`. See
comments inside for help.


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
