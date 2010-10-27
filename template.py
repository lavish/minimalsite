# Author:      Marco Squarcina <lavish@gmail.com>
# Date:        28/10/2010
# Version:     0.4
# License:     MIT, see LICENSE for details

import datetime

# the name of your site
site_name = "My Site"

# your name
author = "Author Name"

# the path under where your site will be shown. For example if you access to
# your site via http://www.domain.com/user/, set prefix = "/user"
prefix = "/"

# the name used for referring to the home page. This variable sets the name for
# the first entry in the navigation path
home = "home"

# the separator character used for the navigation path
path_separator = "/"

# set the extensions used for markdown and textile files
src_ext = {"markdown": "md", "textile": "tt"}

# set the extension used for object files. For example if you plan to embed php
# code you can write "php" here
obj_ext = "html"

# set the list of pages that should be parsed but you don't want to display n
# the menu
hidden = set(["404.md", "500.md", "503.md"])

# set the file name inside your source directory used to determine the last run
# of minimalsite. Set this variable to "" if you want to generate the html
# structure at every invocation of minimalsite
last_run = ".minimalsite_lastrun"

current_time = datetime.datetime.now()

def header(file):
	"""Builds the header and returns it to a string."""

	return '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta content="text/html; charset=UTF-8" http-equiv="content-type" />
		<meta name="author" content="''' + author + '''" />
		<title>''' + site_name + ' | ' + file.split('/')[-1].split('.')[0] + '''</title>
		<link href="''' + prefix + '''/style.css" rel="stylesheet" type="text/css" media="screen" />
	</head>
	<body>
		<div id="container">
			<div id="header">
				<h1>''' + site_name + '''</h1>
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

def footer(file):
	"""Builds the footer and returns it to a string."""

	return '''
				</div>
				<div id="clearer">
					&nbsp;
				</div>
			</div>
			<div id="footer">
				&copy; ''' + str(current_time.year) + ' ' + author + ''' | Generated by <a href="http://www.minimalblue.com/projects/minimalsite.html">minimalsite</a> 
			</div>
		</div>
	</body>
</html>'''
