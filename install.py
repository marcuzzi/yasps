import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="yasps",
    version="0.1.0",
    author="Alejandro Martinez",
    author_email="alejandro.martinez.web@gmail.com",
    description="Yet Another Stock Price Scraper",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/marcuzzi/yasps",
    license="GPL-3.0-or-later",
	data_files=[("", ["LICENSE", ])],
    platforms=["Windows", ],
    packages=find_packages(","),
	install_requires=[
        'beautifulsoup4',
        'pynput',
        'requests',
        'curses'	
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Windows'	
    ],
    python_requires='>=3.6',
)