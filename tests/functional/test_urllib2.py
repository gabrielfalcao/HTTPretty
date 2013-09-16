# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2013>  Gabriel Falcão <gabriel@nacaolivre.org>
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

try:
    from urllib import urlencode
    from urllib.request import urlopen
    import urllib.request as urllib2
except ImportError:
    import urllib2
    urlopen = urllib2.urlopen

from sure import *
from httpretty import HTTPretty, httprettified
from httpretty.core import decode_utf8


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_a_simple_get_with_urllib2_read():
    "HTTPretty should mock a simple GET with urllib2.read()"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    fd = urlopen('http://yipit.com')
    got = fd.read()
    fd.close()

    expect(got).to.equal(b'Find the best daily deals')


@httprettified
@within(two=microseconds)
def test_httpretty_provides_easy_access_to_querystrings(now):
    "HTTPretty should provide an easy access to the querystring"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    fd = urllib2.urlopen('http://yipit.com/?foo=bar&foo=baz&chuck=norris')
    fd.read()
    fd.close()

    expect(HTTPretty.last_request.querystring).to.equal({
        'foo': ['bar', 'baz'],
        'chuck': ['norris'],
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_headers_urllib2(now):
    "HTTPretty should mock basic headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    request = urlopen('http://github.com')

    headers = dict(request.headers)
    request.close()

    expect(request.code).to.equal(201)
    expect(headers).to.equal({
        'content-type': 'text/plain; charset=utf-8',
        'connection': 'close',
        'content-length': '35',
        'status': '201',
        'server': 'Python/HTTPretty',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_urllib2(now):
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

    expect(request.code).to.equal(200)
    expect(headers).to.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_forcing_headers_urllib2():
    "HTTPretty should allow forcing headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                           })

    request = urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    expect(headers).to.equal({
        'content-type': 'application/xml',
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2(now):
    "HTTPretty should allow adding and overwritting headers by " \
    "keyword args with urllib2"

    body = "this is supposed to be the response, indeed"
    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body=body,
                           server='Apache',
                           content_length=len(body),
                           content_type='application/json')

    request = urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    expect(request.code).to.equal(200)
    expect(headers).to.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': str(len(body)),
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_support_a_list_of_successive_responses_urllib2(now):
    "HTTPretty should support adding a list of successive " \
    "responses with urllib2"

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        responses=[
            HTTPretty.Response(body="first response", status=201),
            HTTPretty.Response(body='second and last response', status=202),
        ])

    request1 = urlopen('https://api.yahoo.com/test')
    body1 = request1.read()
    request1.close()

    expect(request1.code).to.equal(201)
    expect(body1).to.equal(b'first response')

    request2 = urlopen('https://api.yahoo.com/test')
    body2 = request2.read()
    request2.close()
    expect(request2.code).to.equal(202)
    expect(body2).to.equal(b'second and last response')

    request3 = urlopen('https://api.yahoo.com/test')
    body3 = request3.read()
    request3.close()
    expect(request3.code).to.equal(202)
    expect(body3).to.equal(b'second and last response')


@httprettified
@within(two=microseconds)
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

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        b'{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(got).to.equal(b'{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(two=microseconds)
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

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        b'{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(got).to.equal(b'{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(two=microseconds)
def test_httpretty_ignores_querystrings_from_registered_uri():
    "HTTPretty should mock a simple GET with urllib2.read()"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/?id=123",
                           body="Find the best daily deals")

    fd = urlopen('http://yipit.com/?id=123')
    got = fd.read()
    fd.close()

    expect(got).to.equal(b'Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/?id=123')


@httprettified
@within(two=microseconds)
def test_callback_response(now):
    ("HTTPretty should all a callback function to be set as the body with"
      " urllib2")

    def request_callback(request, uri, headers):
        return [200, headers, "The {0} response from {1}".format(decode_utf8(request.method), uri)]

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        body=request_callback)

    fd = urllib2.urlopen('https://api.yahoo.com/test')
    got = fd.read()
    fd.close()

    expect(got).to.equal(b"The GET response from https://api.yahoo.com/test")

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

    expect(got).to.equal(b"The POST response from https://api.yahoo.com/test_post")


@httprettified
def test_httpretty_should_allow_registering_regexes():
    "HTTPretty should allow registering regexes with urllib2"

    HTTPretty.register_uri(
        HTTPretty.GET,
        re.compile("https://api.yipit.com/v1/deal;brand=(?P<brand_name>\w+)"),
        body="Found brand",
    )

    request = urllib2.Request(
        "https://api.yipit.com/v1/deal;brand=GAP",
    )
    fd = urllib2.urlopen(request)
    got = fd.read()
    fd.close()

    expect(got).to.equal(b"Found brand")


@httprettified
def test_httpretty_should_check_post_payload():
    "HTTPretty should allow checking POST data payload"

    HTTPretty.register_uri(
        HTTPretty.POST,
        "https://api.imaginary.com/v1/sweet/",
        expected_data={'name': "Lollipop"},
        body='{"id": 12, "status": "Created"}',
    )

    request = urllib2.Request(
        "https://api.imaginary.com/v1/sweet/",
        urlencode({"name": "Lollipop"}),
        {
            'content-type': 'text/json',
        },
    )
    fd = urllib2.urlopen(request)
    got = fd.read()
    fd.close()

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(b'name=Lollipop')
    expect(got).to.equal(b'{"id": 12, "status": "Created"}')

    request = urllib2.Request(
        "https://api.imaginary.com/v1/sweet/",
        urlencode({"wrong": "data"}),
        {
            'content-type': 'text/json',
        },
    )

    try:
        fd = urllib2.urlopen(request)
        got = fd.read()
        fd.close()
        raise Exception("Payload checked didn't work")
    except ValueError:
        pass
