# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2020> Gabriel Falcão <gabriel@nacaolivre.org>
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
import io
import os
from setuptools import setup, find_packages


def read_version():
    ctx = {}
    exec(local_file('httpretty', 'version.py'), ctx)
    return ctx['version']


local_file = lambda *f: \
    io.open(
        os.path.join(os.path.dirname(__file__), *f), encoding='utf-8').read()


install_requires = []
tests_requires = ['nose', 'sure', 'coverage', 'mock;python_version<"3.3"',
                  'rednose']


setup(
    name='httpretty',
    version=read_version(),
    description='HTTP client mock for Python',
    long_description=local_file('README.rst'),
    author='Gabriel Falcao',
    author_email='gabriel@nacaolivre.org',
    url='https://httpretty.readthedocs.io',
    zip_safe=False,
    packages=find_packages(exclude=['*tests*']),
    tests_require=local_file('development.txt').splitlines(),
    install_requires=install_requires,
    license='MIT',
    test_suite='nose.collector',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Testing'
    ],
)
