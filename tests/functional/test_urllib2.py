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
import urllib2
from sure import that, within, microseconds
from httpretty import HTTPretty

@within(two=microseconds)
def test_httpretty_should_mock_a_simple_get_with_urllib2_read():
    u"HTTPretty should mock a simple GET with urllib2.read()"

    HTTPretty.register_uri(HTTPretty.GET, "http://globo.com/",
                           body="The biggest portal in Brazil")

    fd = urllib2.urlopen('http://globo.com')
    got = fd.read()
    fd.close()

    assert that(got).equals('The biggest portal in Brazil')

@within(five=microseconds)
def test_httpretty_should_mock_headers(now):
    u"HTTPretty should mock basic headers"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    assert that(request.code).equals(201)
    assert that(headers).equals({
        'content-type': 'text/plain',
        'connection': 'close',
        'content-length': '35',
        'status': '201 Created',
        'server': 'Python/HTTPretty',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    })


@within(five=microseconds)
def test_httpretty_should_allow_adding_and_overwritting(now):
    u"HTTPretty should allow adding and overwritting headers"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '23456789',
                               'Content-Type': 'application/json',
                           })

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    assert that(request.code).equals(200)
    assert that(headers).equals({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '23456789',
        'status': '200 OK',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    })

@within(five=microseconds)
def test_httpretty_should_allow_forcing_headers():
    u"HTTPretty should allow forcing headers"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                           })

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    assert that(headers).equals({
        'content-type': 'application/xml',
    })


@within(five=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs(now):
    u"HTTPretty should allow adding and overwritting headers by keyword args"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           server='Apache',
                           content_length='23456789',
                           content_type='application/json')

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    assert that(request.code).equals(200)
    assert that(headers).equals({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '23456789',
        'status': '200 OK',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    })

