# MinimalSite

minimalsite is a fast minimal static website builder. It generates web pages
from a file hierarchy with markdown and textile syntax.

                                                   _                
                   o          o                   | |     o         
         _  _  _       _  _       _  _  _    __,  | |  ,    _|_  _  
        / |/ |/ |  |  / |/ |  |  / |/ |/ |  /  |  |/  / \_|  |  |/  
          |  |  |_/|_/  |  |_/|_/  |  |  |_/\_/|_/|__/ \/ |_/|_/|__/



## Requirements

In order to run minimalsite you need a working Python 2.X installation and the
following modules:

* [Python Markdown][] for markdown syntax support
* [PyTextile][] for textile syntax support


## Installation

There's no need to install the tool: download, unpack and run.


## Running minimalsite

Just type from command line:

    ./minimalsite.py <source dir> [output dir]

where "source dir" is the directory containing the source file hierarchy and
"output dir" the directory where you want to create web pages. If you omit to
specify an "output dir", all files will be written inside "source dir".

Please note that you need to place an index file in in each directory you want
to parse.


## Configuration

You can edit "template.py" to fit your needs. See comments inside for help.


## Misc

Please refear to [Markdown Syntax][] and [Textile Syntax][] documentation
before writing your pages.


## Thanks to

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
