from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.7'
DESCRIPTION = 'Anilist Python module that allows you to search up and retrieve anime/manga/characters/etc info. (No login required)'
LONG_DESCRIPTION = "A Python lib that allows the users to directly search up anime/manga related contents through \
                    Anilist. No login is required (user's auth token needed in some cases). The current version of \
                    0.0.7 (alpha testing) is not very stable and certain corner cases have not been checked. \
                    Feel free to report any errors to the labeled email address. The code base can be found at \
                    https://github.com/ReZeroE/AnilistPython"

# Setting up
setup(
    name="AnilistPython",
    version=VERSION,
    author="Kevin L. (ReZeroK)",
    author_email="<kevinliu@vt.edu>",
    license_files = "LICENSE.txt",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'anime', 'anilist', 'manga', 'characters', 'alpha testing', 'Milim', 'ReZeroK'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)