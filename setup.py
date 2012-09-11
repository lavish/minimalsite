import sys
from distutils.core import setup

import minimalsite

setup(
    name = 'minimalsite',
    version = minimalsite.__version__,
    author = minimalsite.__author__,
    author_email = minimalsite.__email__,
    url = 'http://www.minimalblue.com/software/minimalsite.html',
    download_url = 'https://github.com/downloads/lavish/minimalsite/minimalsite-1.00.tar.gz',
    description = minimalsite.__doc__.split('\n')[1],
    long_description = minimalsite.__doc__,
    scripts = ['minimalsite.py'],
    data_files=[('share/minimalsite/templates', ['data/default_template.py', 'data/example_template.py', 'data/style.css'])],
    license = minimalsite.__license__,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Text Processing :: Markup",
    ]
)
