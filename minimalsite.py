#!/usr/bin/python

# Author:      Marco Squarcina <lavish@gmail.com>
# Date:        28/10/2010
# Version:     0.4
# License:     MIT, see LICENSE for details


import os
import codecs
import string
import sys
import template

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

minimalsite_last_run = 0
template_last_change = os.path.getmtime(os.path.join(os.path.split(__file__)[0], "template.py"))

def menu(file, dir):
	"""Given the current directory and the file shown, returns a multiline
	string of the html code for the menu.

	"""

	out = "<ul>\n"
	for entry in sorted(os.listdir(dir)):
		# a hidden file, index, or a symlink
		if(entry[0] == "."
		or entry.startswith("index.")
		or os.path.islink(os.path.join(dir, entry))
		or entry in template.hidden):
			continue
		# a markdown file
		elif(syntax(entry)):
			out += '\t<li><a href="'
			out += entry.split('.')[0]
			if(file.split('/')[-1] == entry):
				out += '.' + template.obj_ext + '" class="current">'
			else:
				out += '.' + template.obj_ext + '">'
			out += entry.split('.')[0]
			out += '</a></li>\n'
		# a directory containing an index file 
		elif(os.path.isdir(os.path.join(dir, entry))
		and (hasindex(os.path.join(dir, entry)))):
			out += '\t<li><a href="'
			out += entry
			out += '/index.' + template.obj_ext + '">'
			out += entry
			out += '/</a></li>\n'
	out += "</ul>"
	return out

def path(file):
	"""Builds the breadcrumb navigation path from the current file shown and
	returns it to a string

	"""

	out = ""
	file_path = file.split('/');
	target_path = sys.argv[1].split('/');
	for i in range(len(target_path)-1, len(file_path)-1):
		if(file_path[i+1].startswith("index.")):
			if(i == len(target_path)-1):
				out += template.home
			else:
				out += ' ' + file_path[i].split('.')[0]
		else:
			out += '<a href="'
			for a in range(2, len(file_path)-i):
				out += '../'
			out += 'index.' + template.obj_ext + '">'
			if(i == len(target_path)-1):
				out += template.home
			else:
				out += file_path[i]
			out += '</a> '
			out += template.path_separator + ' ' 
			if(i+1 == len(file_path)-1):
				out += ' ' + file_path[i+1].split('.')[0]
	return out

def page(file, dir):
	"""Returns the complete html code of a single page."""

	h_src_file = codecs.open(file, "r", "utf-8");
	src_content = h_src_file.read()
	h_src_file.close()
	out = template.header(file)
	if(syntax(file) == "markdown" and "markdown" in template.src_ext):
		out += markdown.markdown(src_content)
	elif(syntax(file) == "textile" and "textile" in template.src_ext):
		out += textile.textile(src_content)
	out += template.footer(file)
	out = out.replace("%%%PATH%%%", path(file))
	out = out.replace("%%%MENU%%%", menu(file, dir))
	return out

def process(dir, margin = ''):
	"""Recursively calls page() on every file/dir in the given directory"""

	for file in os.listdir(dir):
		src_file = os.path.join(dir, file)
		if(os.path.islink(src_file)):
			continue
		elif(os.path.isfile(src_file) and syntax(src_file) and needs_update(dir)):
			out_file = src_file.split('.')
			out_file[-1] = template.obj_ext
			out_file = string.join(out_file, ".")
			if(len(sys.argv) == 3):
				out_file = string.join(sys.argv[2].split('/') + out_file.split('/')[len(sys.argv[1].split('/')):], '/')
				try:
					os.makedirs(string.join(out_file.split('/')[:-1], '/'))
				except OSError:
					pass
			print margin + src_file
			h_out_file = codecs.open(out_file, "w", "utf-8")
			h_out_file.write(page(src_file, dir))
			h_out_file.close()
		elif(os.path.isdir(src_file)):
			process(src_file, margin + '  ')

def syntax(file):
	for lang in template.src_ext.keys():
		if(template.src_ext[lang] == file.split('.')[-1]):
				return lang
	return ''

def hasindex(dir):
	for lang in template.src_ext.keys():
		if(os.path.isfile(dir + "/index." + template.src_ext[lang])):
			return True
	return False

def needs_update(dir):
	if(template_last_change > minimalsite_last_run
	or os.path.getmtime(dir) > minimalsite_last_run):
		return True
	return False

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
			sys.argv[2] = os.path.abspath(sys.argv[2])
		sys.argv[1] = os.path.abspath(sys.argv[1])
		if(template.last_run):
			template.last_run = os.path.join(sys.argv[1], template.last_run)
			if(os.path.isfile(template.last_run)):
				minimalsite_last_run = os.path.getmtime(template.last_run)
		print "Processing files in " + sys.argv[1] + ":\n"
		process(sys.argv[1])
		print "\n... Done!"
		if(template.last_run):
			lastrun_file = open(template.last_run, "w")
			lastrun_file.write("")
			lastrun_file.close()

if __name__ == "__main__":
    main()
