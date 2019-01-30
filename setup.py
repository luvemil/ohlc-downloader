# Instructions from https://gehrcke.de/2014/02/distributing-a-python-command-line-application/

import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('get_ohlc/get_ohlc.py').read(),
    re.M
    ).group(1)

with open("README.md", "r") as f:
    long_descr = f.read()

setup(
    name = "ohlc-downloader",
    packages = ["get_ohlc", "get_ohlc.utils"],
    entry_points = {
        "console_scripts": ['get_ohlc = get_ohlc.get_ohlc:main']
        },
    install_requires=[
        "ccxt",
        "pandas",
        "Click",
        "setuptools",
        "python_dateutil"
    ],
    version = version,
    description = "Python command line application bare bones template.",
    long_description = long_descr,
    long_description_content_type="text/markdown",
    author = "Marco Tarantino",
    author_email = "taran.marco@gmail.com",
    url = "https://github.com/luvemil/ohlc-downloader",
    )
