from setuptools import setup, find_packages

VERSION = '0.0.1'
PACKAGE_NAME = 'ifyfootballdata package'
AUTHOR = 'Ifeanyi Anuebunwa'
AUTHOR_EMAIL = 'jeon316@icloud.com'
URL = 'https://github.com/Jeon316upzx/football-data'
DESCRIPTION = 'Football data package for https://www.football-data.org'
LONG_DESCRIPTION = 'Football data package for https://www.football-data.org'
LICENSE = 'Apache License 2.0'

# Setting up
setup(
    name="ifyfootballdata",
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    url=URL,
    packages=find_packages(),
    install_requires=[],

    keywords=['football-data', 'premier league',
              'La liga', 'Serie A', 'Championship'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
