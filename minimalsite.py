#!/usr/bin/python

# Author:      Marco Squarcina <lavish@gmail.com>
# Date:        04/05/2011
# Version:     0.5
# License:     MIT, see LICENSE for details

import os
import codecs
import string
import sys
import template
import re

try:
	import markdown
except ImportError:
	sys.stderr.write("Module markdown not found.\n")
	del template.src_ext["markdown"]
try:
	import textile
except ImportError:
	sys.stderr.write("Module textile not found.\n")
	del template.src_ext["textile"]


# class definition

class Node(object):
	def __init__(self, src_pathname, parent = None):
		self.src_pathname = src_pathname
		self.dst_pathname = get_dst_pathname(src_pathname)
		self.src_file = os.path.basename(self.src_pathname)
		self.dst_file = os.path.basename(self.dst_pathname)
		self.name = get_name(self.dst_pathname)
		self.parent = parent
		self.children = []

	def add_child(self, obj):
		self.children.append(obj)


# functions definition

def syntax(pathname):
	for lang in template.src_ext.keys():
		if(template.src_ext[lang] == pathname.split('.')[-1]):
				return lang
	return ''

def hasindex(pathname):
	for lang in template.src_ext.keys():
		if(os.path.isfile(pathname + "/index." + template.src_ext[lang])):
			return True
	return False

def get_dst_pathname(src_pathname):
	# replace extension
	dst_pathname = src_pathname.split('.')
	if len(dst_pathname) > 1:
		dst_pathname[-1] = str(template.obj_ext)
	dst_pathname = string.join(dst_pathname, '.')
	# change destination dir
	dst_pathname = string.join(template.dst_dir.split('/') + dst_pathname.split('/')[len(template.src_dir.split('/')):], '/')
	# remove index numbers for dirs and files
	return re.sub('\/\d+_', '/', dst_pathname)

def get_name(dst_pathname):
	name = os.path.basename(dst_pathname)
	name = os.path.splitext(name)[0]
	return name.replace('_', ' ')

def menu(node):
	"""Given the current node, returns a multine string of the menu code."""

	menu = "<ul>\n"
	for n in sorted(node.parent.children, key=lambda n: n.src_pathname):
		# and index page or a hidden file, no need to include them
		if(n.dst_file.startswith("index.")
		or n.src_file in template.hidden):
			continue
		# a page
		elif not n.children:
			menu += '\t<li><a href='
			menu += '"' + n.dst_file + '"'
			# current page
			if(node == n):
				menu += ' class="current"'
			menu += '>' + n.name + '</a></li>\n'
		# a directory
		else:
			menu += '\t<li><a href="'
			menu += n.dst_file
			menu += '/index.' + template.obj_ext + '">'
			menu += n.name + '</a></li>\n'
	menu += "</ul>"
	return menu

def path(node):
	"""Builds the breadcrumb navigation path from the current file shown and
	returns it to a string"""

	# a bit dirty... there's space for improvements
	path = ""
	path_list = []
	j = 0
	while node.parent:
		path_list.append(node.name)
		node = node.parent
	path_list.append(template.home)
	if path_list[0] == "index":
		path_list.remove("index")
	else:
		j = -1
	for i in range(len(path_list)-1, -1, -1):
		if i == 0:
			path += path_list[i]
		else:
			path += '<a href="' + "../" * (i+j) + "index." + template.obj_ext + '">'
			path += path_list[i]
			path += '</a> ' + template.path_separator + ' '
	return path

def write_page(node):
	"""Write a single page"""

	# open source file
	h_src_pathname = codecs.open(node.src_pathname, "r", "utf-8");
	src_content = h_src_pathname.read()
	h_src_pathname.close()
	# create html page
	dst_content = template.header(node)
	if(syntax(node.src_pathname) == "markdown"
	and "markdown" in template.src_ext):
		dst_content += markdown.markdown(src_content)
	elif(syntax(node.src_pathname) == "textile"
	and "textile" in template.src_ext):
		dst_content += textile.textile(src_content)
	dst_content += template.footer(node)
	dst_content = dst_content.replace("%%%PATH%%%", path(node))
	dst_content = dst_content.replace("%%%MENU%%%", menu(node))
	# write html file
	h_dst_pathname = codecs.open(node.dst_pathname, "w", "utf-8")
	h_dst_pathname.write(dst_content)
	h_dst_pathname.close()

def build_tree(node):
	"""Recursively create a tree representing the sources file hierarchy"""

	for file in os.listdir(node.src_pathname):
		pathname = os.path.join(node.src_pathname, file)
		# do not add nodes for links and files starting with '.'
		if(os.path.islink(pathname)
		or file[0] == "."):
			continue
		# add nodes for files with an allowed extension
		elif(os.path.isfile(pathname) and syntax(pathname)):
			node.add_child(Node(pathname, node))
		# add nodes for directories and go on building the tree
		elif(os.path.isdir(pathname) and hasindex(pathname)):
			node.add_child(Node(pathname, node))
			# -1 used to specify the last added node
			build_tree(node.children[-1])

def write_tree(node, margin = ''):
	# a directory
	if node.children:
		# create the destination dir, if possible
		print margin + "creating -> " + node.dst_pathname
		try:
			os.makedirs(node.dst_pathname)
		except OSError:
			pass
		# recursivly call write_tree against current node
		for nodes in node.children:
			write_tree(nodes, margin + '    ')
	# a file
	else:
		print margin + "writing  -> " + node.dst_pathname
		write_page(node)

def main():
	global minimalsite_last_run

	if(len(sys.argv) < 2 or len(sys.argv) > 3):
		sys.stderr.write("Incorrect usage, see -h for help\n")
		sys.exit(1)
	elif(sys.argv[1] == "-h"):
		print '''Usage: minimalsite.py <source dir> [output dir]'''
		sys.exit(0)
	elif(not os.path.isdir(sys.argv[1])):
		sys.stderr.write(sys.argv[1] + " is not a directory, aborting\n")
		sys.exit(2)
	elif(len(sys.argv) == 3 and not os.path.isdir(sys.argv[2])):
		sys.stderr.write(sys.argv[2] + " is not a directory, aborting\n")
		sys.exit(2)
	elif(not template.src_ext):
		sys.stderr.write("No modules for parsing files found. See README for requirements\n")
		sys.exit(3)
	else:
		if(len(sys.argv) == 3):
			template.dst_dir = os.path.abspath(sys.argv[2])
		template.src_dir = os.path.abspath(sys.argv[1])
		if(template.last_run):
			template.last_run = os.path.join(template.src_dir, template.last_run)
			if(os.path.isfile(template.last_run)):
				minimalsite_last_run = os.path.getmtime(template.last_run)
		print "Processing files in " + template.src_dir + ":\n"
		root = Node(template.src_dir)
		build_tree(root)
		write_tree(root)
		print "\n... Done!"
		if(template.last_run):
			lastrun_file = open(template.last_run, "w")
			lastrun_file.write("")
			lastrun_file.close()

if __name__ == "__main__":
    main()
