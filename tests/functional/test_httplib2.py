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

import httplib2
from sure import expect, within, microseconds
from httpretty import HTTPretty, httprettified


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_a_simple_get_with_httplib2_read(now):
    u"HTTPretty should mock a simple GET with httplib2.context.http"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    _, got = httplib2.Http().request('http://yipit.com', 'GET')
    expect(got).to.equal('Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/')


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_headers_httplib2(now):
    u"HTTPretty should mock basic headers with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    headers, _ = httplib2.Http().request('http://github.com', 'GET')
    expect(headers['status']).to.equal('201')
    expect(dict(headers)).to.equal({
        'content-type': 'text/plain; charset=utf-8',
        'connection': 'close',
        'content-length': '35',
        'status': '201',
        'server': 'Python/HTTPretty',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_httplib2(now):
    u"HTTPretty should allow adding and overwritting headers with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '27',
                               'Content-Type': 'application/json',
                           })

    headers, _ = httplib2.Http().request('http://github.com/foo', 'GET')

    expect(dict(headers)).to.equal({
        'content-type': 'application/json',
        'content-location': 'http://github.com/foo',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_forcing_headers_httplib2(now):
    u"HTTPretty should allow forcing headers with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="this is supposed to be the response",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                           })

    headers, _ = httplib2.Http().request('http://github.com/foo', 'GET')

    expect(dict(headers)).to.equal({
        'content-location': 'http://github.com/foo',  # httplib2 FORCES
                                                   # content-location
                                                   # even if the
                                                   # server does not
                                                   # provide it
        'content-type': 'application/xml',
        'status': '200',  # httplib2 also ALWAYS put status on headers
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2(now):
    u"HTTPretty should allow adding and overwritting headers by keyword args " \
        "with httplib2"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="this is supposed to be the response",
                           server='Apache',
                           content_length='27',
                           content_type='application/json')

    headers, _ = httplib2.Http().request('http://github.com/foo', 'GET')

    expect(dict(headers)).to.equal({
        'content-type': 'application/json',
        'content-location': 'http://github.com/foo',  # httplib2 FORCES
                                                   # content-location
                                                   # even if the
                                                   # server does not
                                                   # provide it
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_rotating_responses_with_httplib2(now):
    u"HTTPretty should support rotating responses with httplib2"

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        responses=[
            HTTPretty.Response(body="first response", status=201),
            HTTPretty.Response(body='second and last response', status=202),
        ])

    headers1, body1 = httplib2.Http().request(
        'https://api.yahoo.com/test', 'GET')

    expect(headers1['status']).to.equal('201')
    expect(body1).to.equal('first response')

    headers2, body2 = httplib2.Http().request(
        'https://api.yahoo.com/test', 'GET')

    expect(headers2['status']).to.equal('202')
    expect(body2).to.equal('second and last response')

    headers3, body3 = httplib2.Http().request(
        'https://api.yahoo.com/test', 'GET')

    expect(headers3['status']).to.equal('202')
    expect(body3).to.equal('second and last response')


@httprettified
@within(two=microseconds)
def test_can_inspect_last_request(now):
    u"HTTPretty.last_request is a mimetools.Message request from last match"

    HTTPretty.register_uri(HTTPretty.POST, "http://api.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    headers, body = httplib2.Http().request(
        'http://api.github.com', 'POST',
        body='{"username": "gabrielfalcao"}',
        headers={
            'content-type': 'text/json',
        },
    )

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        '{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(body).to.equal('{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(two=microseconds)
def test_can_inspect_last_request_with_ssl(now):
    u"HTTPretty.last_request is recorded even when mocking 'https' (SSL)"

    HTTPretty.register_uri(HTTPretty.POST, "https://secure.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    headers, body = httplib2.Http().request(
        'https://secure.github.com', 'POST',
        body='{"username": "gabrielfalcao"}',
        headers={
            'content-type': 'text/json',
        },
    )

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        '{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(body).to.equal('{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(two=microseconds)
def test_httpretty_ignores_querystrings_from_registered_uri(now):
    u"Registering URIs with query string cause them to be ignored"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/?id=123",
                           body="Find the best daily deals")

    _, got = httplib2.Http().request('http://yipit.com/?id=123', 'GET')

    expect(got).to.equal('Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/?id=123')


@httprettified
@within(two=microseconds)
def test_callback_response(now):
    (u"HTTPretty should all a callback function to be set as the body with"
      " httplib2")

    def request_callback(method, uri, headers):
        return "The {} response from {}".format(method, uri)

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        body=request_callback)

    headers1, body1 = httplib2.Http().request(
        'https://api.yahoo.com/test', 'GET')

    expect(body1).to.equal('The GET response from https://api.yahoo.com/test')

    HTTPretty.register_uri(
        HTTPretty.POST, "https://api.yahoo.com/test_post",
        body=request_callback)

    headers2, body2 = httplib2.Http().request(
        'https://api.yahoo.com/test_post', 'POST')

    expect(body2).to.equal('The POST response from https://api.yahoo.com/test_post')
