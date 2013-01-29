# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from sure import *
from httpretty import HTTPretty, httprettified


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_a_simple_get_with_urllib2_read():
    u"HTTPretty should mock a simple GET with urllib2.read()"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    fd = urllib2.urlopen('http://yipit.com')
    got = fd.read()
    fd.close()

    expect(got).to.equal('Find the best daily deals')


@httprettified
@within(two=microseconds)
def test_httpretty_provides_easy_access_to_querystrings(now):
    u"HTTPretty should provide an easy access to the querystring"

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
    u"HTTPretty should mock basic headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    request = urllib2.urlopen('http://github.com')

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
    u"HTTPretty should allow adding and overwritting headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '27',
                               'Content-Type': 'application/json',
                           })

    request = urllib2.urlopen('http://github.com')
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
    u"HTTPretty should allow forcing headers with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                           })

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    expect(headers).to.equal({
        'content-type': 'application/xml',
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2(now):
    u"HTTPretty should allow adding and overwritting headers by " \
    "keyword args with urllib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response, indeed",
                           server='Apache',
                           content_length='111111',
                           content_type='application/json')

    request = urllib2.urlopen('http://github.com')
    headers = dict(request.headers)
    request.close()

    expect(request.code).to.equal(200)
    expect(headers).to.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '111111',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_support_a_list_of_successive_responses_urllib2(now):
    u"HTTPretty should support adding a list of successive " \
    "responses with urllib2"

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        responses=[
            HTTPretty.Response(body="first response", status=201),
            HTTPretty.Response(body='second and last response', status=202),
        ])

    request1 = urllib2.urlopen('https://api.yahoo.com/test')
    body1 = request1.read()
    request1.close()

    expect(request1.code).to.equal(201)
    expect(body1).to.equal('first response')

    request2 = urllib2.urlopen('https://api.yahoo.com/test')
    body2 = request2.read()
    request2.close()
    expect(request2.code).to.equal(202)
    expect(body2).to.equal('second and last response')

    request3 = urllib2.urlopen('https://api.yahoo.com/test')
    body3 = request3.read()
    request3.close()
    expect(request3.code).to.equal(202)
    expect(body3).to.equal('second and last response')


@httprettified
@within(two=microseconds)
def test_can_inspect_last_request(now):
    u"HTTPretty.last_request is a mimetools.Message request from last match"

    HTTPretty.register_uri(HTTPretty.POST, "http://api.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    request = urllib2.Request(
        'http://api.github.com',
        '{"username": "gabrielfalcao"}',
        {
            'content-type': 'text/json',
        },
    )
    fd = urllib2.urlopen(request)
    got = fd.read()
    fd.close()

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        '{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(got).to.equal('{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(two=microseconds)
def test_can_inspect_last_request_with_ssl(now):
    u"HTTPretty.last_request is recorded even when mocking 'https' (SSL)"

    HTTPretty.register_uri(HTTPretty.POST, "https://secure.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    request = urllib2.Request(
        'https://secure.github.com',
        '{"username": "gabrielfalcao"}',
        {
            'content-type': 'text/json',
        },
    )
    fd = urllib2.urlopen(request)
    got = fd.read()
    fd.close()

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        '{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(got).to.equal('{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(two=microseconds)
def test_httpretty_ignores_querystrings_from_registered_uri():
    u"HTTPretty should mock a simple GET with urllib2.read()"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/?id=123",
                           body="Find the best daily deals")

    fd = urllib2.urlopen('http://yipit.com/?id=123')
    got = fd.read()
    fd.close()

    expect(got).to.equal('Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/?id=123')
