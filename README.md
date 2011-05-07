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

Just type from command line:

    ./minimalsite.py [source_dir [destination_dir]]

where source\_dir is the directory containing the source file hierarchy and
destination\_dir the directory where you want to create web pages. If you omit
to specify a destionation\_dir, all files will be written inside source\_dir.
You can also specify these directories editing the template file.

Please note that you need to place an index file in in each directory you want
to parse.


### Configuration

You can edit "template.py" to fit your needs. See comments inside for help.


### Extra Features

#### Page ordering

If you need to order menu entries, you can add a numerical index before the
pathname, for example:

	/home/marco/website/30_university.md
	/home/marco/website/50_contacts.md

will be written as:

	/var/www/marco/htdocs/university.html
	/var/www/marco/htdocs/contacts.html

and "university" will be displayed before "contacts" in the menu. Both files and
directories are supported.


### Misc

Please refear to [Markdown Syntax][] and [Textile Syntax][] documentation before writing your pages.


### Thanks to

* [Anselm R Garbe][], providing the idea behind this tool ([genosite][])
* [Luca Postregna][], testing and lots of useful suggestions
* Josie Panzuto, linguistic revision
* [Emanuele Giaquinta][], some tips


[Python Markdown]:    http://www.freewisdom.org/projects/python-markdown
[PyTextile]:          http://loopcore.com/python-textile/
[Markdown Syntax]:    http://daringfireball.net/projects/markdown/syntax
[Textile Syntax]:     http://en.wikipedia.org/wiki/Textile_(markup_language)
[Anselm R Garbe]:     http://garbe.us/
[genosite]:           http://hg.suckless.org/genosite/
[Luca Postregna]:     http://luca.postregna.name/
[Emanuele Giaquinta]: http://tomaw.net/~exg/
