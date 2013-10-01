# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from httpretty import version, HTTPretty
from setuptools import setup

HTTPretty.disable()

HTTPRETTY_PATH = os.path.abspath(os.path.join(__file__, os.pardir))


def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk(os.path.join(HTTPRETTY_PATH, 'httpretty')):
        path = root.replace(HTTPRETTY_PATH, '').strip('/')
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(path)).strip("."))

    return packages


def test_packages():
    test_reqs = os.path.join(HTTPRETTY_PATH, 'requirements.pip')
    tests_require = [
            line.strip() for line in open(test_reqs).readlines()
            if not line.startswith("#")
        ]
    return tests_require

setup(name='httpretty',
    version=version,
    description='HTTP client mock for Python',
    author='Gabriel Falcao',
    author_email='gabriel@nacaolivre.org',
    url='http://github.com/gabrielfalcao/httpretty',
    zip_safe=False,
    packages=get_packages(),
    tests_require=test_packages(),
    install_requires=['urllib3'],
    license='MIT',
    classifiers=["Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Topic :: Software Development :: Testing"],
)
