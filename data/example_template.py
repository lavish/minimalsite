import time
import datetime

# the name of your site
SITE_NAME = "My HTML5 Website"

# your name
AUTHOR = "Marco Squarcina"

# source dir containing the markup file hierarchy, like
# "/home/marco/website/src". It is not mandatory to set this value here, you
# can specify the value of this variable at runtime, see minimalsite.py -h
SRC = ""

# destination dir for your site, usually under the webroot pathname, like
# "/var/www/marco/htdocs". It is not mandatory to set this value here, you can
# specify the value of this variable at runtime, see minimalsite.py -h
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
PATH_SEPARATOR = '<span class="separator">/</span>'

# set the extensions used for markdown, textile and plain files that don't need
# to be parsed
SRC_EXT = {"markdown": "md", "textile": "tt", "plain": "txt"}


# set the extension used for destination files. For example if you plan to
# embed php code you can write "php" here
DST_EXT = "html"

# set the list of pages that should be parsed but you don't want to display n
# the menu
HIDDEN = set(["404.md", "500.md", "search.md"])

# specify title and description for the following pages
PAGES = {SRC + "/foo.md": ("Adventures of Foo", "Read everything about the mighty adventures of Foo in the World of Baz!"),
         SRC + "/bar.md": ("All about Bar", "It's a sad story, but worth reading...")}

# global variable for storing menu code
menu_code = ''

def get_page_contents(node):
    """Return page title and description from the global variable pages if a
    match with current node page.src_pathname is found.
    """ 

    try:
        return (SITE_NAME + ' | ' + PAGES[node.page.src_pathname][0], \
            PAGES[node.page.src_pathname][1])
    except KeyError:
        return ('%%%TITLE%%%', '')

def menu(node):
    """Generate a hierarchical menu."""

    global menu_code

    menu_code = '\n'
    root = node
    while root.parent:
        root = root.parent
    menu_(root, node)
    return menu_code

def menu_(node, cur_node, node_prefix = PREFIX, indent = ''):
    """Auxiliary recursive function for menu generation."""

    global menu_code

    menu_code += indent + '<ul>\n'
    for child in sorted(node.children, key=lambda n: n.page.src_pathname):
        if child.page.dst_file.startswith("index.") or child.page.src_file in HIDDEN:
            continue
        menu_code += indent + '<li class="level-' + str(child.page.level) + '"><a '
        if(child == cur_node
        or (cur_node.page.dst_file.startswith("index.") and child == cur_node.parent)):
            menu_code += 'class="current" '
        menu_code += 'href="' + node_prefix + child.page.dst_file
        if child.children:
            menu_code += "/index." + DST_EXT + '">'    + child.page.name + '</a>\n'
            menu_(child, cur_node, node_prefix + child.page.dst_file + '/', indent + '\t')
            menu_code += indent + '</li>\n'
        else:
            menu_code += '">'   + child.page.name + '</a></li>\n'
    menu_code += indent + '</ul>\n'

def header(node):
    """Build the header and return it to a string."""

    (title, description) = get_page_contents(node)
    return '''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="author" content="''' + AUTHOR + '''" />
        <meta name="generator" content="minimalsite-%%%VERSION%%%" />
        <meta name="description" content="''' + description + '''" />
        <title>''' + title + '''</title>
        <link rel="shortcut icon" href="/favicon.ico" />
        <style type="text/css">
            #container {
                width: 80%;
                margin: 30px auto;
            }
            #content {
                margin-left: 170px;
                text-align: justify;
            }
            #edit {
                clear: both;
                text-align: right;
                font-size: small;
            }
            footer {
                clear: both;
            }
            nav {
                float: left;
                width: 160px;
            }
            nav li a.current {
                background-color: blue;
                color: #ffffff;
                font-weight: bold;
            }
            nav ul {
                margin: 0;
                padding: 0;
                list-style: none;
                width: 150px; /* Width of Menu Items */
                border-bottom: 1px solid #ccc;
            }
            nav ul li {
                position: relative;
            }
            nav li ul {
                position: absolute;
                left: 149px; /* Set 1px less than menu width */
                top: 0;
                display: none;
            }
            /* Styles for Menu Items */
            nav ul li a {
                display: block;
                text-decoration: none;
                color: #777;
                background: #fff; /* IE6 Bug */
                padding: 5px;
                border: 1px solid #ccc; /* IE6 Bug */
                border-bottom: 0;
            }
            /* Holly Hack. IE Requirement \*/
            * html ul li { float: left; height: 1%; }
            * html ul li a { height: 1%; }
            /* End */
            nav li:hover ul, li.over ul { display: block; } /* The magic */
        </style>
    </head>
    <body>
        <div id="container">
            <header>
                <h1><a href="''' + '../' * node.page.level + '''index.''' + DST_EXT + '''">''' + SITE_NAME + '''</a></h1>
            </header>
            <div id="path">
                You are here: %%%PATH%%%
            </div>
            <div id="main">
                <nav>
                    ''' + menu(node) + '''
                </nav>
                <div id="content">
'''

def footer(node):
    """Build the footer and return it to a string."""

    current_time = datetime.datetime.now()
    return '''
                </div>
                <div id="edit">
                    Last edit: ''' + time.strftime("%m/%d/%Y %I:%M:%S %p", node.page.last_edit) + '''
                </div>
            </div>
            <footer>
                &copy; ''' + str(current_time.year) + ' ' + AUTHOR + ''' | Generated with <a href="http://www.minimalblue.com/projects/minimalsite.html">minimalsite</a> 
            </footer>
        </div>
    </body>
</html>'''
