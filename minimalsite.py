#!/usr/bin/env python

"""
A fast minimal static website builder.

Minimalsite generates web pages from a source file hierarchy. It supports
markdown and textile syntax, but plain txt and html can be evenly used.
Template files are python modules, providing huge flexibilty and keeping the
codebase tiny and simple.

"""

import os
import re
import sys
import imp
import time
import string
import codecs
import argparse

try:
    import markdown
except ImportError:
    pass
try:
    import textile
except ImportError:
    pass

__author__      = "Marco Squarcina <lavish at gmail.com>"
__license__     = "MIT"
__copyright__   = "Copyright 2012, Marco Squarcina"
__status__      = "Development"
__version__     = "0.99"


# class definitions

class Page:
    """
    Meta informations of a page.
    
    Attributes:

        src_pathname    pathname of the source file 
        dst_pathname    pathname of the generated file
        src_file        file name of the source file
        dst_file        file name of the generated file
        name            file name of the generated file without extension
        level           depth level in the site hierarchy
        last_edit       time.struct_time date of source file last edit
    """

    def __init__(self, src_pathname, level):
        self.src_pathname = src_pathname
        self.dst_pathname = self._get_dst_pathname()
        self.src_file = os.path.basename(self.src_pathname)
        self.dst_file = os.path.basename(self.dst_pathname)
        self.name = self._get_name()
        self.level = level
        self.last_edit = time.localtime(os.path.getmtime(self.src_pathname))

    def _get_dst_pathname(self):
        """Get destination pathname from source pathname."""

        # replace extension
        dst_pathname = os.path.splitext(self.src_pathname)
        if dst_pathname[1]:
            dst_pathname = os.path.join(dst_pathname[0] + '.' + template.dst_ext)
        dst_pathname = ''.join(dst_pathname)
        # change destination dir
        dst_pathname = '/'.join(template.dst.split('/')
            + dst_pathname.split('/')[len(template.src.split('/')):])
        # remove index numbers for dirs and files
        return re.sub('\/\d+_', '/', dst_pathname)

    def _get_name(self):
        """Get page name from destionation pathname."""

        name = os.path.basename(self.dst_pathname)
        name = os.path.splitext(name)[0]
        return name.replace('_', ' ')

    def __str__(self):
        """Return a textual representation of the page."""

        data = "<{}, {}, {}, {}, {}, {}>"
        return data.format(self.src_pathname, self.dst_pathname, \
            self.src_file, self.dst_file, self.name, self.level)

class TreeNode:
    """
    Node of the site hierarchy tree structure.

    Attributes:

        page        Page object
        parent      parent node, None if current node is the root
        children    list of children

    """

    def __init__(self, page, parent = None):
        self.page = page
        self.parent = parent
        self.children = []

    def build(self):
        """Create the site tree, representing the source file hierarchy."""

        # check if src dir includes an index file
        if self.page.level == 0 \
        and not self._has_index(template.src):
            die('Directory {} does not include a valid index file, aborting.'\
                .format(template.src), 2)

        for file in os.listdir(self.page.src_pathname):
            pathname = os.path.join(self.page.src_pathname, file)
            # do not add nodes for links and files starting with '.'
            if os.path.islink(pathname) or file[0] == ".":
                continue
            # add nodes for files with an allowed extension
            elif os.path.isfile(pathname) and self._syntax(pathname):
                node = TreeNode(Page(pathname, self.page.level + 1), self)
                self.children.append(node)
            # add nodes for directories and go on building the tree
            elif os.path.isdir(pathname) and self._has_index(pathname):
                node = TreeNode(Page(pathname, self.page.level + 1), self)
                self.children.append(node)
                node.build()

    def write(self, margin = ''):
        """Write the generated site on the file system."""

        # a directory
        if self.children:
            # create the destination dir, if possible
            try:
                os.makedirs(self.page.dst_pathname)
            except OSError:
                pass
            else:
                print(margin + self.page.dst_pathname)
            # recursivly call write_tree against current node
            for child in self.children:
                child.write(margin + '    ')
        # a file
        else:
            print(margin + self.page.dst_pathname)
            self._write_page()

    def title(self):
        """Return the title for the current node."""
    
        if self.page.name == 'index':
            page_name = self.parent.page.name
        else:
            page_name = self.page.name
        return template.site_name + ' | ' + page_name

    def menu(self):
        """Return the generated code for menu."""

        menu_code = "<ul>\n"
        for sibling in sorted(self.parent.children, key=lambda sibling: sibling.page.src_pathname):
            # and index page or a hidden file, no need to include them
            if sibling.page.dst_file.startswith("index.") or sibling.page.src_file in template.hidden:
                continue
            # a page
            elif not sibling.children:
                menu_code += '\t<li><a href="{}"'.format(sibling.page.dst_file)
                # current page
                if self == sibling:
                    menu_code += ' class="current"'
                menu_code += '>{}</a></li>\n'.format(sibling.page.name)
            # a directory
            else:
                menu_code += '\t<li><a href="{}/index.{}">{}</a></li>\n' \
                    .format(sibling.page.dst_file, template.dst_ext, sibling.page.name)
        menu_code += "</ul>"
        return menu_code

    def path(self):
        """Return the generated code for breadcrumb navigation path."""
        
        path = ""
        path_node = []
        tmp_node = self
        while tmp_node:
            path_node.insert(0, tmp_node)
            tmp_node = tmp_node.parent
        # no need to display "index" in the path
        if path_node[-1].page.name == "index":
            path_node.pop()
        for i in range(0, len(path_node)):
            # last item, it could be current page or current dir
            if i == len(path_node) - 1:
                path += path_node[i].page.name
            # a parent page
            else:
                traversal = "../" * (self.page.level - path_node[i].page.level - 1)
                path += '<a href="{}index.{}">{}</a> {} ' \
                    .format(traversal, template.dst_ext, path_node[i].page.name, template.path_separator)
        return path

    def write_sitemap(self):
        """Write an XML sitemap to the file system."""

        fp = open(template.sitemap, 'w')
        fp.write('{}\n{}\n{}{}'.format('<?xml version="1.0" encoding="UTF-8"?>', \
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', \
            self._get_sitemap_entries(template.url + template.prefix), \
            '</urlset>'))
        fp.close()
        
    def _get_sitemap_entries(self, prefix):
        """Recursively return the XML entry for sitemap."""

        xml = ""
        if self.children:
            for child in self.children:
                if not child.page.src_file in template.hidden:
                    if self.page.level:
                        xml += child._get_sitemap_entries(prefix + self.page.dst_file + '/')
                    else:
                        xml += child._get_sitemap_entries(prefix)
        else:
            xml = "  <url>\n    <loc>{}</loc>\n    <lastmod>{}</lastmod>\n  </url>\n" \
                .format(prefix + self.page.dst_file, time.strftime("%Y-%m-%d", self.page.last_edit))
        return xml

    def _write_page(self):
        """Write a single page on the file system."""

        # open source file
        h_src_pathname = codecs.open(self.page.src_pathname, "r", "utf-8");
        src_content = h_src_pathname.read()
        h_src_pathname.close()
        # build page
        dst_content = template.header(self)
        if self._syntax(self.page.src_pathname) == "markdown" \
        and "markdown" in template.src_ext:
            dst_content += markdown.markdown(src_content)
        elif self._syntax(self.page.src_pathname) == "textile" \
        and "textile" in template.src_ext:
            dst_content += textile.textile(src_content)
        elif self._syntax(self.page.src_pathname) == "plain" \
        and "plain" in template.src_ext:
            dst_content += src_content
        dst_content += template.footer(self)
        dst_content = dst_content.replace("%%%TITLE%%%", self.title())
        dst_content = dst_content.replace("%%%PATH%%%", self.path())
        dst_content = dst_content.replace("%%%MENU%%%", self.menu())
        dst_content = dst_content.replace("%%%VERSION%%%", __version__)
        # write destionation file
        h_dst_pathname = codecs.open(self.page.dst_pathname, "w", "utf-8")
        h_dst_pathname.write(dst_content)
        h_dst_pathname.close()

    def _syntax(self, pathname):
        """Return the markup language used in the given pathname."""

        for lang in list(template.src_ext.keys()):
            if template.src_ext[lang] == pathname.split('.')[-1]:
                    return lang

    def _has_index(self, pathname):
        """Check if there's an index file in the given directory pathname."""

        for lang in list(template.src_ext.keys()):
            if os.path.isfile(pathname + "/index." + template.src_ext[lang]):
                return True
        return False

    def __str__(self):
        """Return the entire tree structure."""

        tree = "    " * self.page.level + str(self.page) + "\n"
        for child in self.children:
            tree += str(child)
        return tree


# function definitions

def import_template(pathname):
    """Load the python module in the provided file name as a template."""

    if not os.path.isfile(pathname):
        die("Template file does not exist. Aborting.")
    (path, name) = os.path.split(pathname)
    (name, ext) = os.path.splitext(name)
    if ext == '.py' and name.endswith('_template'):
        (fd, pathname, data) = imp.find_module(name, [path])
        return imp.load_module(name, fd, pathname, data)
    else:
        die("Invalid template file name. Valid templates must terminate with '_template.py'.")

def check_template():
    """Check mandatory variable/function definitions in the provided template."""

    template_data = dir(template)
    required_data = ['dst', 'dst_ext', 'footer', 'header', 'hidden', 'home', \
        'path_separator', 'prefix', 'sitemap', 'site_name', 'src', 'src_ext', 'url']
    for data in required_data:
        if not data in template_data:
            die("Missing {} definition in template file. Aborting.".format(data))

def notice(msg):
    """Write a notice message to stdout."""

    print("[*] {}".format(msg))

def die(msg, code=1):
    """Write an error message to stderr and exit."""

    sys.stderr.write("[!] {}\n".format(msg))
    sys.exit(code)

def main():
    global template

    parser = argparse.ArgumentParser(description='Fast minimal static website builder')
    parser.add_argument('-t', '--template', type=str, required=True, \
        help="specify a template file name. Valid templates must terminate with '_template.py'")
    parser.add_argument('-V', '--verbose', action='store_true', \
        default=False, help='verbosely display site structure')
    parser.add_argument('-s', '--src', type=str, default=None, \
        help='source dir, where the textual hierarchy resides')
    parser.add_argument('-d', '--dst', type=str, default=None, \
        help='destination dir, where the html pages will be written')
    parser.add_argument('-m', '--sitemap', type=str, default=None, \
        help='full path name for the XML sitemap')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s-'+__version__)
    args = parser.parse_args()

    # load template
    template = import_template(args.template)
    # check template integrity
    check_template()
    # check markup modules
    for markup in ('markdown', 'textile'):
        if not markup in sys.modules:
            del template.src_ext[markup]
    if not template.src_ext:
        die("No modules for parsing files found. See README for requirements.")
    # check src and dst directories
    if args.src:
        template.src = args.src
    if args.dst:
        template.dst = args.dst
    # assign sitemap pathname
    if args.sitemap:
        template.sitemap = args.sitemap
    # fix trailing slashes
    template.src = os.path.abspath(template.src)
    template.dst = os.path.abspath(template.dst)
    for directory in [template.src, template.dst]:
        if not os.path.isdir(directory):
            die('Directory {} does not exist, aborting.'.format(directory), 2)
    # start writing pages
    notice('Processing files from {}'.format(template.src))
    root = TreeNode(Page(template.src, 0))
    root.page.name = template.home
    root.build()
    notice('Writing {} files into {}'.format(template.dst_ext, template.dst))
    root.write()
    # write sitemap
    if template.sitemap:
        notice('Writing sitemap to {}'.format(template.sitemap))
        root.write_sitemap()
    if args.verbose:
        notice('Printing site structure')
        notice('values as: <src_pathname, dst_pathname, src_file, dst_file, name, level>')
        print(root)

if __name__ == "__main__":
    main()
