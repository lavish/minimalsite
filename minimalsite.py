#!/usr/bin/python

# Author:      Marco Squarcina <lavish@gmail.com>
# License:     MIT, see LICENSE for details

import getopt, os, sys
import string, codecs, re

try:
	import markdown
except ImportError:
	sys.stderr.write("Module markdown not found.\n")
try:
	import textile
except ImportError:
	sys.stderr.write("Module textile not found.\n")


# class definition

class Node(object):
	def __init__(self, src_pathname, level, parent = None):
		self.src_pathname = src_pathname
		self.dst_pathname = get_dst_pathname(src_pathname)
		self.src_file = os.path.basename(self.src_pathname)
		self.dst_file = os.path.basename(self.dst_pathname)
		self.name = get_name(self.dst_pathname)
		self.level = level
		self.parent = parent
		self.children = []

	def __str__(self):
		s  = '<%s:%s, ' % ('src_pathname', self.src_pathname)
		s += '%s:%s, '  % ('dst_pathname', self.dst_pathname)
		s += '%s:%s, '  % ('src_file', self.src_file)
		s += '%s:%s, '  % ('dst_file', self.dst_file)
		s += '%s:%s, '  % ('name', self.name)
		s += '%s:%d>\n' % ('level', self.level)
		return s

	def add_child(self, obj):
		self.children.append(obj)


# functions definition

def syntax(pathname):
	"""Returns the markup language used in the given pathname."""

	for lang in list(template.src_ext.keys()):
		if template.src_ext[lang] == pathname.split('.')[-1]:
				return lang
	return ''

def hasindex(pathname):
	"""Check if there's an index file in the given directory pathname."""

	for lang in list(template.src_ext.keys()):
		if os.path.isfile(pathname + "/index." + template.src_ext[lang]):
			return True
	return False

def get_dst_pathname(src_pathname):
	"""Get destionation pathname from source pathname."""

	# replace extension
	dst_pathname = os.path.splitext(src_pathname)
	if dst_pathname[1]:
		dst_pathname = os.path.join(dst_pathname[0] + '.' + template.dst_ext)
	dst_pathname = ''.join(dst_pathname)
	# change destination dir
	dst_pathname = string.join(template.dst_dir.split('/')
		+ dst_pathname.split('/')[len(template.src_dir.split('/')):], '/')
	# remove index numbers for dirs and files
	return re.sub('\/\d+_', '/', dst_pathname)

def get_name(dst_pathname):
	"""Get page name from destionation pathname."""

	name = os.path.basename(dst_pathname)
	name = os.path.splitext(name)[0]
	return name.replace('_', ' ')

def menu(node):
	"""Given a node, returns a multine string of the menu code."""

	menu_code = "<ul>\n"
	for sibling in sorted(node.parent.children, key=lambda sibling: sibling.src_pathname):
		# and index page or a hidden file, no need to include them
		if sibling.dst_file.startswith("index.") or sibling.src_file in template.hidden:
			continue
		# a page
		elif not sibling.children:
			menu_code += '\t<li><a href='
			menu_code += '"' + sibling.dst_file + '"'
			# current page
			if node == sibling:
				menu_code += ' class="current"'
			menu_code += '>' + sibling.name + '</a></li>\n'
		# a directory
		else:
			menu_code += '\t<li><a href="'
			menu_code += sibling.dst_file
			menu_code += '/index.' + template.dst_ext + '">'
			menu_code += sibling.name + '</a></li>\n'
	menu_code += "</ul>"
	return menu_code

def path(node):
	"""Given a node, returns a string of the breadcrumb navigation path code."""
	
	path = ""
	path_node = []
	tmp_node = node
	while tmp_node:
		path_node.insert(0, tmp_node)
		tmp_node = tmp_node.parent
	# no need to display "index" in the path
	if path_node[-1].name == "index":
		path_node.pop()
	for i in range(0, len(path_node)):
		# last item, it could be current page or current dir
		if i == len(path_node) - 1:
			path += path_node[i].name
		# a parent page
		else:
			path += '<a href="'
			path += "../" * (node.level - path_node[i].level - 1)
			path += "index." + template.dst_ext + '">'
			path += path_node[i].name 
			path += '</a> ' + template.path_separator + ' '
	return path

def write_page(node):
	"""Given a node, write on the file system its corresponding page."""

	# open source file
	h_src_pathname = codecs.open(node.src_pathname, "r", "utf-8");
	src_content = h_src_pathname.read()
	h_src_pathname.close()
	# build page
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
	# write destionation file
	h_dst_pathname = codecs.open(node.dst_pathname, "w", "utf-8")
	h_dst_pathname.write(dst_content)
	h_dst_pathname.close()

def print_tree(node, margin = ''):
	"""Given a node, display the entire tree structure from that node."""

	if node:
		sys.stderr.write(margin + str(node)) 
		for child in node.children:
			print_tree(child, margin + '    ')

def build_tree(node):
	"""Given a node, recursively create a tree representing the sources file
	hierarchy starting from that node."""

	for file in os.listdir(node.src_pathname):
		pathname = os.path.join(node.src_pathname, file)
		# do not add nodes for links and files starting with '.'
		if os.path.islink(pathname) or file[0] == ".":
			continue
		# add nodes for files with an allowed extension
		elif os.path.isfile(pathname) and syntax(pathname):
			node.add_child(Node(pathname, node.level + 1, node))
		# add nodes for directories and go on building the tree
		elif os.path.isdir(pathname) and hasindex(pathname):
			node.add_child(Node(pathname, node.level + 1, node))
			# -1 used to specify the last added node
			build_tree(node.children[-1])

def write_tree(node, margin = ''):
	"""Given a node, recursively write all the corresponding pages on the file
	system."""

	# a directory
	if node.children:
		# create the destination dir, if possible
		try:
			os.makedirs(node.dst_pathname)
		except OSError:
			pass
		else:
			print(margin + "creating -> " + node.dst_pathname)
		# recursivly call write_tree against current node
		for child in node.children:
			write_tree(child, margin + '    ')
	# a file
	else:
		print(margin + "writing  -> " + node.dst_pathname)
		write_page(node)

def main():
	global template

	# set default arguments
	src_dir = dst_dir = None
	template_module = 'templates.default'
	verbose = False
	# parse options
	try:
		opts, args = getopt.getopt(sys.argv[1:], 
			"ht:s:d:Vv", 
			["help", "template=", "src_dir=", "dst_dir=", "version", "verbose"])
	except getopt.GetoptError as err:
		sys.stderr.write('Incorrect usage, see -h for help\n')
		sys.exit(1)
	for o, a in opts:
		if o in ("-V", "--version"):
			print('minimalsite-0.7 by Marco Squarcina, see LICENSE for details')
			sys.exit(0)
		elif o in ("-h", "--help"):
			print('''Usage: minimalsite.py [options]

Options:
  -h, --help                     Show help options
  -V, --version                  Display minimalsite version
  -v, --verbose                  Display the entire tree structure
  -t, --template=TEMPLATE        Specify a template
  -s, --src_dir=SOURCE_DIR       Specify source dir to use
  -d, --dst_dir=DESTINATION_DIR  Specify destionation dir to use''')
			sys.exit(0)
		elif o in ("-t", "--template"):
			template_module = 'templates.' + a
		elif o in ("-s", "--src_dir"):
			src_dir = a
		elif o in ("-d", "--dst_dir"):
			dst_dir = a
		elif o in ("-v", "--verbose"):
			verbose = True
		else:
			assert False, "unhandled option"
	# load template
	__import__(template_module)
	template = sys.modules[template_module]
	# check markup modules
	for markup in ('markdown', 'textile'):
		if not markup in sys.modules:
			del template.src_ext[markup]
	if not template.src_ext:
		sys.stderr.write("No modules for parsing files found. See README for requirements\n")
		sys.exit(3)
	# check src and dst directories
	if src_dir:
		template.src_dir = os.path.abspath(src_dir)
	if dst_dir:
		template.dst_dir = os.path.abspath(dst_dir)
	if not os.path.isdir(template.src_dir):
		sys.stderr.write('"' + template.src_dir + '" is not a directory, aborting\n')
		sys.exit(2)
	if not os.path.isdir(template.dst_dir):
		sys.stderr.write('"' + template.dst_dir + '" is not a directory, aborting\n')
		sys.exit(2)
	# check if src dir includes an index file
	if not hasindex(template.src_dir):
		sys.stderr.write('"' + template.src_dir + '" does not include a valid index file, aborting\n')
		sys.exit(2)
	# start writing pages
	print('Processing files in "' + template.src_dir + '":\n')
	root = Node(template.src_dir, 0)
	root.name = template.home
	build_tree(root)
	write_tree(root)
	print('\n... Done!')
	if verbose:
		sys.stderr.write("\nSite structure:\n\n")
		print_tree(root)

if __name__ == "__main__":
    main()
