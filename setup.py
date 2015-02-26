#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011>  Gabriel Falcao <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import os
import re
import codecs
from setuptools import setup, find_packages


def read_version():
    """Read version from httpretty/version.py without loading any files"""
    contents = local_file('httpretty', '__init__.py')
    return re.compile(r".*__version__ = version = '(.*?)'", re.S).match(contents).group(1)


def parse_requirements(path):
    """Rudimentary parser for the `requirements/use.txt` file

    We just want to separate regular packages from links to pass them to the
    `install_requires` and `dependency_links` params of the `setup()`
    function properly.
    """
    try:
        requirements = (line.strip() for line in local_file(path).splitlines())
    except IOError:
        raise RuntimeError("Couldn't find the `requirements/use.txt' file :(")

    links = []
    pkgs = []
    for req in requirements:
        if not req:
            continue
        if 'http:' in req or 'https:' in req:
            links.append(req)
            name, version = re.findall("\#egg=([^\-]+)-(.+$)", req)[0]
            pkgs.append('{0}=={1}'.format(name, version))
        else:
            pkgs.append(req)

    return pkgs, links


def local_file(*f):
    with codecs.open(os.path.join(os.path.dirname(__file__), *f), encoding='utf-8') as fd:
        return fd.read()


install_requires, dependency_links = \
    parse_requirements('requirements/use.txt')


setup(
    name='httpretty',
    version=read_version(),
    description='HTTP client mock for Python',
    long_description=local_file('README.rst'),
    author='Gabriel Falcao',
    author_email='gabriel@nacaolivre.org',
    url='http://github.com/gabrielfalcao/httpretty',
    zip_safe=False,
    packages=find_packages(exclude=['*tests*']),
    tests_require=parse_requirements('requirements/test.txt')[0],
    install_requires=install_requires,
    dependency_links=dependency_links,
    license='MIT',
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Testing'
    ],
)
