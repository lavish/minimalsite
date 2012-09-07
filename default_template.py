import datetime

# the name of your site
site_name = "My Site"

# your name
author = "Author Name"

# source dir containing the markup file hierarchy, like
# "/home/marco/website/src". It is not mandatory to set this value here, you
# can specify the value of this variable at runtime, see 'minimalsite -h'
src = ""

# destination dir for your site, usually under the webroot pathname, like
# "/var/www/marco/htdocs". It is not mandatory to set this value here, you can
# specify the value of this variable at runtime, see 'minimalsite -h'
dst = ""

# specify a file name for the XML sitemap. If blank, no sitemap will be written
# on the filesystem. It's also possible to set this parameter at runtime using
# 'minimalsite -m'
sitemap = ""

# the url of your site. Mainly used for sitemap generation
url = "http://www.example.org"

# the path under where your site will be shown. For example if you access to
# your site via http://www.domain.com/user/, set prefix = "/user/"
prefix = "/"

# the name used for referring to the home page. This variable sets the name for
# the first entry in the navigation path
home = "home"

# the separator character used for the navigation path
path_separator = "/"

# set the extensions used for markdown, textile and plain files that don't need
# to be parsed
src_ext = {"markdown": "md", "textile": "tt", "plain": "txt"}

# set the extension used for destination files. For example if you plan to
# embed php code you can write "php" here
dst_ext = "html"

# set the list of pages that should be parsed but you don't want to display n
# the menu
hidden = set(["404.md", "500.md", "404.tt", "500.tt", "400.txt", "500.txt"])


current_time = datetime.datetime.now()

def header(node):
    """Build the header and return it to a string."""

    return '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
        <meta name="author" content="''' + author + '''" />
        <meta name="generator" content="minimalsite-%%%VERSION%%%" />
        <title>%%%TITLE%%%</title>
        <link href="''' + '../' * (node.page.level-1) + '''style.css" rel="stylesheet" type="text/css" media="screen" />
    </head>
    <body>
        <div id="container">
            <div id="header">
                <h1><a href="''' + '../' * (node.page.level-1) + '''index.''' + dst_ext + '''">''' + site_name + '''</a></h1>
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

    return '''
                </div>
                <div id="clearer">
                    &nbsp;
                </div>
            </div>
            <div id="footer">
                &copy; ''' + str(current_time.year) + ' ' + author + ''' | Generated with <a href="http://www.minimalblue.com/projects/minimalsite.html">minimalsite</a> 
            </div>
        </div>
    </body>
</html>'''
