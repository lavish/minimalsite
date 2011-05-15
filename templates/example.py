# Author:      Marco Squarcina <lavish@gmail.com>
# License:     MIT, see LICENSE for details

import os
import time, datetime

# the name of your site
site_name = "My HTML5 Website"

# your name
author = "Marco Squarcina"

# source dir containing the markup file hierarchy, like
# "/home/marco/website/src". It is not mandatory to set this value here, you
# can specify the value of this variable at runtime, see minimalsite.py -h
src_dir = ""

# destination dir for your site, usually under the webroot pathname, like
# "/var/www/marco/htdocs". It is not mandatory to set this value here, you can
# specify the value of this variable at runtime, see minimalsite.py -h
dst_dir = ""

# the path under where your site will be shown. For example if you access to
# your site via http://www.domain.com/user/, set prefix = "/user/"
prefix = "/"

# the name used for referring to the home page. This variable sets the name for
# the first entry in the navigation path
home = "home"

# the separator character used for the navigation path
path_separator = '<span class="separator">/</span>'

# set the extensions used for markdown and textile files
src_ext = {"markdown": "md", "textile": "tt"}

# set the extension used for destination files. For example if you plan to
# embed php code you can write "php" here
dst_ext = "html"

# set the list of pages that should be parsed but you don't want to display n
# the menu
hidden = set(["404.md", "500.md", "404.tt", "500.tt", "search.md"])


current_time = datetime.datetime.now()
menu_code = ''

def menu(node):
	global menu_code

	menu_code = '\n'
	root = node
	while root.parent:
		root = root.parent
	menu_(root, node)
	return menu_code

def menu_(node, cur_node, node_prefix = prefix, indent = ''):
	global menu_code

	menu_code += indent + '<ul>\n'
	for child in sorted(node.children, key=lambda n: n.src_pathname):
		if child.dst_file.startswith("index.") or child.src_file in hidden:
			continue
		menu_code += indent + '<li class="level-' + str(child.level) + '"><a '
		if(child == cur_node
		or (cur_node.dst_file.startswith("index.") and child == cur_node.parent)):
			menu_code += 'class="current" '
		menu_code += 'href="' + node_prefix + child.dst_file
		if child.children:
			menu_code += "/index." + dst_ext + '">'	+ child.name + '</a>\n'
			menu_(child, cur_node, node_prefix + child.dst_file + '/', indent + '\t')
			menu_code += indent + '</li>\n'
		else:
			menu_code += '">'   + child.name + '</a></li>\n'
	menu_code += indent + '</ul>\n'

def header(node):
	"""Builds the header and returns it to a string."""
	
	return '''<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<meta name="author" content="''' + author + '''" />
		<title>''' + site_name + ' | ' + node.name + '''</title>
		<link rel="shortcut icon" href="/favicon.ico" />
		<style type="text/css">
			nav {
				float: left;
				width: 25%;
			}
			nav ul,
			nav li {
				margin: 0;
				padding: 0;
				list-style: none;
			}
			nav li {
				padding-left: 2em;
			}
			nav li.level-1 {
				padding: 0;
			}
			nav li a {
				text-decoration: none;
			}
			nav li a.current {
				text-decoration: underline;
				font-weight: bold;
			}
			#content {
				float: right;
				width: 74%;
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
		</style>
	</head>
	<body>
		<div id="container">
			<header>
				<h1><a href="''' + '../' * node.level + '''index.''' + dst_ext + '''">''' + site_name + '''</a></h1>
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
	"""Builds the footer and returns it to a string."""

	return '''
				</div>
				<div id="edit">
					Last edit: ''' + time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(os.path.getmtime(node.src_pathname))) + '''
				</div>
			</div>
			<footer>
				&copy; ''' + str(current_time.year) + ' ' + author + ''' | Generated by <a href="http://www.minimalblue.com/projects/minimalsite.html">minimalsite</a> 
			</footer>
		</div>
	</body>
</html>'''
