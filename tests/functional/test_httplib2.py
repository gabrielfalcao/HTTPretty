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

import httplib2
from sure import *
from httpretty import HTTPretty

def setup(context):
    HTTPretty.enable()
    context.http = httplib2.Http()

def teardown(context):
    HTTPretty.enable()
    context.http = httplib2.Http()

@within(two=microseconds)
@that_with_context(setup, teardown)
def test_httpretty_should_mock_a_simple_get_with_httplib2_read(context, now):
    u"HTTPretty should mock a simple GET with httplib2.context.http"

    HTTPretty.register_uri(HTTPretty.GET, "http://globo.com/",
                           body="The biggest portal in Brazil")

    _, got = context.http.request('http://globo.com', 'GET')
    assert that(got).equals('The biggest portal in Brazil')

@within(two=microseconds)
@that_with_context(setup, teardown)
def test_httpretty_should_mock_headers_httplib2(context, now):
    u"HTTPretty should mock basic headers with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    headers, _ = context.http.request('http://github.com', 'GET')
    assert that(headers['status']).equals('201')
    assert that(headers).equals({
        'content-type': 'text/plain',
        'connection': 'close',
        'content-length': '35',
        'status': '201',
        'server': 'Python/HTTPretty',
        'date': now.strftime('%a, %d %b %Y %H:%M:%SGMT')
    })


@within(two=microseconds)
@that_with_context(setup, teardown)
def test_httpretty_should_allow_adding_and_overwritting_httplib2(context, now):
    u"HTTPretty should allow adding and overwritting headers with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '27',
                               'Content-Type': 'application/json',
                           })

    headers, _ = context.http.request('http://github.com', 'GET')

    assert that(headers).equals({
        'content-type': 'application/json',
        'content-location': 'http://github.com/',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    })

@within(two=microseconds)
@that_with_context(setup, teardown)
def test_httpretty_should_allow_forcing_headers_httplib2(context, now):
    u"HTTPretty should allow forcing headers with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                           })

    headers, _ = context.http.request('http://github.com', 'GET')

    assert that(headers).equals({
        'content-location': 'http://github.com/', # httplib2 FORCES content-location even if the server does not provide it
        'content-type': 'application/xml',
        'status': '200', # httplib2 also ALWAYS put status on headers
    })


@within(two=microseconds)
@that_with_context(setup, teardown)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2(context, now):
    u"HTTPretty should allow adding and overwritting headers by keyword args " \
        "with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           server='Apache',
                           content_length='27',
                           content_type='application/json')

    headers, _ = context.http.request('http://github.com', 'GET')

    assert that(headers).equals({
        'content-type': 'application/json',
        'content-location': 'http://github.com/', # httplib2 FORCES content-location even if the server does not provide it
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    })


@within(two=microseconds)
@that_with_context(setup, teardown)
def test_httpretty_should_support_a_list_of_successive_responses_httplib2(context, now):
    u"HTTPretty should support adding a list of successive responses with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/gabrielfalcao/httpretty",
                           responses=[
                               HTTPretty.Response(body="first response", status=201),
                               HTTPretty.Response(body='second and last response', status=202),
                            ])


    headers1, body1 = context.http.request('http://github.com/gabrielfalcao/httpretty', 'GET')

    assert that(headers1['status']).equals('201')
    assert that(body1).equals('first response')

    headers2, body2 = context.http.request('http://github.com/gabrielfalcao/httpretty', 'GET')

    assert that(headers2['status']).equals('202')
    assert that(body2).equals('second and last response')

    headers3, body3 = context.http.request('http://github.com/gabrielfalcao/httpretty', 'GET')

    assert that(headers3['status']).equals('202')
    assert that(body3).equals('second and last response')

