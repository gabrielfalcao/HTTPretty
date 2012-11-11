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

import requests
from sure import that, within, microseconds, expect
from httpretty import HTTPretty, httprettified


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_a_simple_get_with_requests_read(now):
    u"HTTPretty should mock a simple GET with requests.get"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    response = requests.get('http://yipit.com')
    assert that(response.text).equals('Find the best daily deals')
    assert that(HTTPretty.last_request.method).equals('GET')
    assert that(HTTPretty.last_request.path).equals('/')


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_headers_requests(now):
    u"HTTPretty should mock basic headers with requests"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    response = requests.get('http://github.com')
    assert that(response.status_code).equals(201)

    assert that(dict(response.headers)).equals({
        'content-type': 'text/plain; charset=utf-8',
        'connection': 'close',
        'content-length': '35',
        'status': '201',
        'server': 'Python/HTTPretty',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_requests(now):
    u"HTTPretty should allow adding and overwritting headers with requests"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '27',
                               'Content-Type': 'application/json',
                           })

    response = requests.get('http://github.com/foo')

    assert that(dict(response.headers)).equals({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_forcing_headers_requests(now):
    u"HTTPretty should allow forcing headers with requests"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="<root><baz /</root>",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                               'Content-Length': '19',
                           })

    response = requests.get('http://github.com/foo')

    assert that(dict(response.headers)).equals({
        'content-type': 'application/xml',
        'content-length': '19',
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2(now):
    u"HTTPretty should allow adding and overwritting headers by keyword args " \
        "with requests"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="this is supposed to be the response",
                           server='Apache',
                           content_length='27',
                           content_type='application/json')

    response = requests.get('http://github.com/foo')

    assert that(dict(response.headers)).equals({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_rotating_responses_with_requests(now):
    u"HTTPretty should support rotating responses with requests"

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        responses=[
            HTTPretty.Response(body="first response", status=201),
            HTTPretty.Response(body='second and last response', status=202),
        ])

    response1 = requests.get(
        'https://api.yahoo.com/test')

    assert that(response1.status_code).equals(201)
    assert that(response1.text).equals('first response')

    response2 = requests.get(
        'https://api.yahoo.com/test')

    assert that(response2.status_code).equals(202)
    assert that(response2.text).equals('second and last response')

    response3 = requests.get(
        'https://api.yahoo.com/test')

    assert that(response3.status_code).equals(202)
    assert that(response3.text).equals('second and last response')


@httprettified
@within(two=microseconds)
def test_can_inspect_last_request(now):
    u"HTTPretty.last_request is a mimetools.Message request from last match"

    HTTPretty.register_uri(HTTPretty.POST, "http://api.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    response = requests.post(
        'http://api.github.com',
        '{"username": "gabrielfalcao"}',
        headers={
            'content-type': 'text/json',
        },
    )

    assert that(HTTPretty.last_request.method).equals('POST')
    assert that(HTTPretty.last_request.body).equals(
        '{"username": "gabrielfalcao"}',
    )
    assert that(HTTPretty.last_request.headers['content-type']).equals(
        'text/json',
    )
    assert that(response.json).equals({"repositories": ["HTTPretty", "lettuce"]})


@httprettified
@within(two=microseconds)
def test_can_inspect_last_request_with_ssl(now):
    u"HTTPretty.last_request is recorded even when mocking 'https' (SSL)"

    HTTPretty.register_uri(HTTPretty.POST, "https://secure.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    response = requests.post(
        'https://secure.github.com',
        '{"username": "gabrielfalcao"}',
        headers={
            'content-type': 'text/json',
        },
    )

    assert that(HTTPretty.last_request.method).equals('POST')
    assert that(HTTPretty.last_request.body).equals(
        '{"username": "gabrielfalcao"}',
    )
    assert that(HTTPretty.last_request.headers['content-type']).equals(
        'text/json',
    )
    assert that(response.json).equals({"repositories": ["HTTPretty", "lettuce"]})


@httprettified
@within(two=microseconds)
def test_httpretty_ignores_querystrings_from_registered_uri(now):
    u"HTTPretty should ignore querystrings from the registered uri (requests library)"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/?id=123",
                           body="Find the best daily deals")

    response = requests.get('http://yipit.com/', params={'id': 123})
    expect(response.text).to.equal('Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/?id=123')
