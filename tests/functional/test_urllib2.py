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
from __future__ import unicode_literals

import re
try:
    from urllib.request import urlopen
    import urllib.request as urllib2
except ImportError:
    import urllib2
    urlopen = urllib2.urlopen

from freezegun import freeze_time
from sure import within, miliseconds
from httpretty import HTTPretty, httprettified
from httpretty.core import decode_utf8


@httprettified
@within(two=miliseconds)
def test_httpretty_should_mock_a_simple_get_with_urllib2_read():
    "HTTPretty should mock a simple GET with urllib2.read()"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    fd = urlopen('http://yipit.com')
    got = fd.read()
    fd.close()

    got.should.equal(b'Find the best daily deals')


@httprettified
@within(two=miliseconds)
def test_httpretty_provides_easy_access_to_querystrings(now):
    "HTTPretty should provide an easy access to the querystring"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    fd = urllib2.urlopen('http://yipit.com/?foo=bar&foo=baz&chuck=norris')
    fd.read()
    fd.close()

    HTTPretty.last_request.querystring.should.equal({
        'foo': ['bar', 'baz'],
        'chuck': ['norris'],
    })


@httprettified
@freeze_time("2013-10-04 04:20:00")
def test_httpretty_should_mock_headers_urllib2():
    "HTTPretty should mock basic headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    request = urlopen('http://github.com')

    headers = dict(request.headers)
    request.close()

    request.code.should.equal(201)
    headers.should.equal({
        'content-type': 'text/plain; charset=utf-8',
        'connection': 'close',
        'content-length': '35',
        'status': '201',
        'server': 'Python/HTTPretty',
        'date': 'Fri, 04 Oct 2013 04:20:00 GMT',
    })


@httprettified
@freeze_time("2013-10-04 04:20:00")
def test_httpretty_should_allow_adding_and_overwritting_urllib2():
    "HTTPretty should allow adding and overwritting headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '27',
                               'Content-Type': 'application/json',
                           })

    request = urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    request.code.should.equal(200)
    headers.should.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': 'Fri, 04 Oct 2013 04:20:00 GMT',
    })


@httprettified
@within(two=miliseconds)
def test_httpretty_should_allow_forcing_headers_urllib2():
    "HTTPretty should allow forcing headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                               'Content-Length': '35a',
                           })

    request = urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    headers.should.equal({
        'content-type': 'application/xml',
        'content-length': '35a',
    })


@httprettified
@freeze_time("2013-10-04 04:20:00")
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2():
    ("HTTPretty should allow adding and overwritting headers by "
     "keyword args with urllib2")

    body = "this is supposed to be the response, indeed"
    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body=body,
                           server='Apache',
                           content_length=len(body),
                           content_type='application/json')

    request = urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    request.code.should.equal(200)
    headers.should.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': str(len(body)),
        'status': '200',
        'server': 'Apache',
        'date': 'Fri, 04 Oct 2013 04:20:00 GMT',
    })


@httprettified
@within(two=miliseconds)
def test_httpretty_should_support_a_list_of_successive_responses_urllib2(now):
    ("HTTPretty should support adding a list of successive "
     "responses with urllib2")

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        responses=[
            HTTPretty.Response(body="first response", status=201),
            HTTPretty.Response(body='second and last response', status=202),
        ])

    request1 = urlopen('https://api.yahoo.com/test')
    body1 = request1.read()
    request1.close()

    request1.code.should.equal(201)
    body1.should.equal(b'first response')

    request2 = urlopen('https://api.yahoo.com/test')
    body2 = request2.read()
    request2.close()
    request2.code.should.equal(202)
    body2.should.equal(b'second and last response')

    request3 = urlopen('https://api.yahoo.com/test')
    body3 = request3.read()
    request3.close()
    request3.code.should.equal(202)
    body3.should.equal(b'second and last response')


@httprettified
@within(two=miliseconds)
def test_can_inspect_last_request(now):
    "HTTPretty.last_request is a mimetools.Message request from last match"

    HTTPretty.register_uri(HTTPretty.POST, "http://api.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    request = urllib2.Request(
        'http://api.github.com',
        b'{"username": "gabrielfalcao"}',
        {
            'content-type': 'text/json',
        },
    )
    fd = urlopen(request)
    got = fd.read()
    fd.close()

    HTTPretty.last_request.method.should.equal('POST')
    HTTPretty.last_request.body.should.equal(
        b'{"username": "gabrielfalcao"}',
    )
    HTTPretty.last_request.headers['content-type'].should.equal(
        'text/json',
    )
    got.should.equal(b'{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(two=miliseconds)
def test_can_inspect_last_request_with_ssl(now):
    "HTTPretty.last_request is recorded even when mocking 'https' (SSL)"

    HTTPretty.register_uri(HTTPretty.POST, "https://secure.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    request = urllib2.Request(
        'https://secure.github.com',
        b'{"username": "gabrielfalcao"}',
        {
            'content-type': 'text/json',
        },
    )
    fd = urlopen(request)
    got = fd.read()
    fd.close()

    HTTPretty.last_request.method.should.equal('POST')
    HTTPretty.last_request.body.should.equal(
        b'{"username": "gabrielfalcao"}',
    )
    HTTPretty.last_request.headers['content-type'].should.equal(
        'text/json',
    )
    got.should.equal(b'{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(two=miliseconds)
def test_httpretty_ignores_querystrings_from_registered_uri():
    "HTTPretty should mock a simple GET with urllib2.read()"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/?id=123",
                           body="Find the best daily deals")

    fd = urlopen('http://yipit.com/?id=123')
    got = fd.read()
    fd.close()

    got.should.equal(b'Find the best daily deals')
    HTTPretty.last_request.method.should.equal('GET')
    HTTPretty.last_request.path.should.equal('/?id=123')


@httprettified
@within(two=miliseconds)
def test_callback_response(now):
    ("HTTPretty should call a callback function to be set as the body with"
     " urllib2")

    def request_callback(request, uri, headers):
        return [200, headers, "The {} response from {}".format(decode_utf8(request.method), uri)]

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        body=request_callback)

    fd = urllib2.urlopen('https://api.yahoo.com/test')
    got = fd.read()
    fd.close()

    got.should.equal(b"The GET response from https://api.yahoo.com/test")

    HTTPretty.register_uri(
        HTTPretty.POST, "https://api.yahoo.com/test_post",
        body=request_callback)

    request = urllib2.Request(
        "https://api.yahoo.com/test_post",
        b'{"username": "gabrielfalcao"}',
        {
            'content-type': 'text/json',
        },
    )
    fd = urllib2.urlopen(request)
    got = fd.read()
    fd.close()

    got.should.equal(b"The POST response from https://api.yahoo.com/test_post")


@httprettified
def test_httpretty_should_allow_registering_regexes():
    "HTTPretty should allow registering regexes with urllib2"

    HTTPretty.register_uri(
        HTTPretty.GET,
        re.compile(r"https://api.yipit.com/v1/deal;brand=(?P<brand_name>\w+)"),
        body="Found brand",
    )

    request = urllib2.Request(
        "https://api.yipit.com/v1/deal;brand=GAP",
    )
    fd = urllib2.urlopen(request)
    got = fd.read()
    fd.close()

    got.should.equal(b"Found brand")
