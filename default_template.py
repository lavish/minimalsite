import datetime

# the name of your site
SITE_NAME = "My Site"

# your name
AUTHOR = "Author Name"

# source dir containing the markup file hierarchy, like
# "/home/marco/website/src". It is not mandatory to set this value here, you
# can specify the value of this variable at runtime, see 'minimalsite -h'
SRC = ""

# destination dir for your site, usually under the webroot pathname, like
# "/var/www/marco/htdocs". It is not mandatory to set this value here, you can
# specify the value of this variable at runtime, see 'minimalsite -h'
DST = ""

# specify a file name for the XML sitemap. If blank, no sitemap will be written
# on the filesystem. It's also possible to set this parameter at runtime using
# 'minimalsite -m'
SITEMAP = ""

# the url of your site. Mainly used for sitemap generation
URL = "http://www.example.org"

# the path under where your site will be shown. For example if you access to
# your site via http://www.domain.com/user/, set prefix = "/user/"
PREFIX = "/"

# the name used for referring to the home page. This variable sets the name for
# the first entry in the navigation path
HOME = "home"

# the separator character used for the navigation path
PATH_SEPARATOR = "/"

# set the extensions used for markdown, textile and plain files that don't need
# to be parsed
SRC_EXT = {"markdown": "md", "textile": "tt", "plain": "txt"}

# set the extension used for destination files. For example if you plan to
# embed php code you can write "php" here
DST_EXT = "html"

# set the list of pages that should be parsed but you don't want to display n
# the menu
HIDDEN = set(["404.md", "500.md", "404.tt", "500.tt", "400.txt", "500.txt"])


def header(node):
    """Build the header and return it to a string."""

    return '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
        <meta name="author" content="''' + AUTHOR + '''" />
        <meta name="generator" content="minimalsite-%%%VERSION%%%" />
        <title>%%%TITLE%%%</title>
        <link href="''' + '../' * (node.page.level-1) + '''style.css" rel="stylesheet" type="text/css" media="screen" />
    </head>
    <body>
        <div id="container">
            <div id="header">
                <h1><a href="''' + '../' * (node.page.level-1) + '''index.''' + DST_EXT + '''">''' + SITE_NAME + '''</a></h1>
            </div>
            <div id="path">
                You are here: %%%PATH%%%
            </div>
            <div id="main">
                <div id="menu">
%%%MENU%%%
                </div>
                <div id="content">
'''

def footer(node):
    """Build the footer and return it to a string."""

    current_time = datetime.datetime.now()
    return '''
                </div>
                <div id="clearer">
                    &nbsp;
                </div>
            </div>
            <div id="footer">
                &copy; ''' + str(current_time.year) + ' ' + AUTHOR + ''' | Generated with <a href="http://www.minimalblue.com/projects/minimalsite.html">minimalsite</a> 
            </div>
        </div>
    </body>
</html>'''
