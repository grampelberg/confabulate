#
# Copyright(c) 2010, Thomas Rampelberg <thomas@saunter.org>
# All rights reserved.
#

__date__ = "%date%"
__version__ = "%version%"

from setuptools import find_packages, setup

setup(
    name = 'confabulate',
    author = 'Thomas Rampelberg',
    author_email = 'thomas@saunter.org',
    version = '0.1',
    packages = find_packages(),
    install_requires = ['pycurl', 'simplejson', 'tornado'],
)
