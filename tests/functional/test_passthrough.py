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
import requests
from unittest import skip
from sure import expect

from httpretty import HTTPretty


@skip
def test_http_passthrough():
    url = 'http://httpbin.org/status/200'
    response1 = requests.get(url)

    response1 = requests.get(url, stream=True)

    HTTPretty.enable()
    HTTPretty.register_uri(HTTPretty.GET, 'http://google.com/', body="Not Google")

    response2 = requests.get('http://google.com/')
    expect(response2.content).to.equal(b'Not Google')

    response3 = requests.get(url, stream=True)
    (response3.content).should.equal(response1.content)

    HTTPretty.disable()

    response4 = requests.get(url, stream=True)
    (response4.content).should.equal(response1.content)


@skip
def test_https_passthrough():
    url = 'https://raw.githubusercontent.com/gabrielfalcao/HTTPretty/master/COPYING'

    response1 = requests.get(url, stream=True)

    HTTPretty.enable()
    HTTPretty.register_uri(HTTPretty.GET, 'https://google.com/', body="Not Google")

    response2 = requests.get('https://google.com/')
    expect(response2.content).to.equal(b'Not Google')

    response3 = requests.get(url, stream=True)
    (response3.content).should.equal(response1.content)

    HTTPretty.disable()

    response4 = requests.get(url, stream=True)
    (response4.content).should.equal(response1.content)
