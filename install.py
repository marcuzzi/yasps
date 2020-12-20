from distutils.core import setup
import setuptools
import os

# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, ‘README.md’), encoding=’utf-8′) as f:
        long_description = f.read()
except Exception:
    long_description = ”

setuptools.setup(
    name="yasps",
    version="0.1.0",
    author="Alejandro Martinez",
    author_email="alejandro.martinez.web@gmail.com",
    description="Yet Another Stock Price Scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcuzzi/yasps",
    license="GPL-3.0-or-later",
	data_files=[("", ["LICENSE.txt", ])],
    platforms=["Windows", ],
    packages=setuptools.find_packages(","),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Windows'	
    ],
    python_requires='>=3.6',
)