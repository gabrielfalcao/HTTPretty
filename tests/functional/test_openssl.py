# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2015>  Gabriel Falcão <gabriel@nacaolivre.org>
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
import socket


from urlparse import urlparse
from OpenSSL import SSL
from httplib import HTTPConnection, HTTPS_PORT

from sure import expect, within, microseconds
from httpretty import HTTPretty, httprettified
from httpretty.core import decode_utf8


CRLF = str('\r\n')


class OpenSSLConnection(HTTPConnection):
    """
    This class allows communication via SSL using PyOpenSSL. It is a drop in
    replacement for httplib.HTTPSConnection, but optionally allows a ssl context
    to be passed.

    For host, port, key_file, cert_file, strict, timeout, source_address
    see httplib.HTTPConnection

    @param ssl_ctx: optional ssl_ctx to pass in
    @type ssl_ctx: OpenSSL.SSL.Context
    @see: https://github.com/shanemhansen/pyopenssl_httplib/blob/master/pyopenssl_httplib.py
    """

    default_port = HTTPS_PORT

    def __init__(self, host, port=None, key_file=None, cert_file=None,
                 strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                 source_address=None, ssl_ctx=None):

        HTTPConnection.__init__(self, host, port, strict, timeout, source_address)

        self.key_file = key_file
        self.cert_file = cert_file

        if ssl_ctx is None:
            ssl_ctx = SSL.Context(SSL.SSLv23_METHOD)
        if self.key_file is not None:
            ssl_ctx.use_privatekey_file(self.key_file)
        if self.cert_file is not None:
            ssl_ctx.use_certificate_file(self.cert_file)
            ssl_ctx.use_certificate_chain_file(self.cert_file)

        self.ssl_ctx = ssl_ctx

    def connect(self):
        """
        Create SSL socket and connect to peer. Note this uses
        socket.create_connection which is ip6 friendly.
        """
        sock = socket.create_connection((self.host, self.port),
                                        self.timeout, self.source_address)
        self.sock = Connection(self.ssl_ctx, sock)
        self.sock.set_connect_state()

    def close(self):
        """Close socket and shutdown SSL connection"""
        self.sock.close()


class Connection(object):
    """
    Proxy to OpenSSL.SSL.Connection containing support for the .makefile()
    method.

    Rationale: The pyopenssl documentation states that
    OpenSSL.SSL.Connection.makefile raises a NotImplemented error because
    there are no .dup semantics for SSL connections which *is* the documented
    behaviour of of socket.makefile, but the documentation is incorrect.
    See: http://bugs.python.org/issue14303

    We can use the logic in socket._fileobject to implement .makefile(),
    allowing pyopenssl to play nice with python's httplib.
    """
    __slots__ = ["_conn"]

    def __init__(self, ctx, conn):
        self._conn = SSL.Connection(ctx, conn)

    def __getattr__(self, attr):
        return getattr(self._conn, attr)

    def makefile(self, *args):
        return socket._fileobject(self, *args)


def request(url, method, body=None, headers=None):
    """
    This is a mock HTTP client which uses pyOpenSSL for SSL, it's based on
    the one found inside the w3af project, but it could be any client using
    pyOpenSSL instead of python's "ssl" module

    This function consumes only a sub-set of all the available
    OpenSSL.SSL.Context / OpenSSL.SSL.Connection methods, but it's enough to
    test the basics. If in the future you wish to add support for more pyopenssl
    methods you should also add them here to make sure they do work as expected.

    This code should never be used in production! It's just for testing, doesn't
    have any kind of error handling nor respects the RFCs!

    :param url: The URL to retrieve
    :param method: The HTTP method
    :param body: The HTTP request body (aka post-data)
    :param headers: The HTTP request headers
    :return: A tuple containing HTTP response headers and the response body
    """
    parsed_url = urlparse(url)

    location = '/' if parsed_url.path is '' else parsed_url.path

    if parsed_url.query:
        location += '?%s' % parsed_url.query

    if parsed_url.params:
        location += ';' + parsed_url.params

    hostname = str(parsed_url.hostname)

    port = 80
    if parsed_url.port is not None:
        port = parsed_url.port
    elif url.lower().startswith('https://'):
        port = 443

    headers = {} if headers is None else headers

    conn = OpenSSLConnection(hostname, port)
    conn.request(method, location, body=body, headers=headers)

    response = conn.getresponse()
    body = response.read()

    response_headers = dict(response.getheaders())
    response_headers['status'] = str(response.status)

    return response_headers, body


@httprettified
@within(ten=microseconds)
def test_httpretty_should_mock_a_simple_get_with_pyopenssl_read(now):
    "HTTPretty should mock a simple GET"

    HTTPretty.register_uri(HTTPretty.GET, "https://yipit.com/",
                           body="Find the best daily deals")

    _, got = request('https://yipit.com', 'GET')
    expect(got).to.equal(b'Find the best daily deals')

    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/')


@httprettified
@within(ten=microseconds)
def test_httpretty_provides_easy_access_to_querystrings(now):
    "HTTPretty should provide an easy access to the querystring"

    HTTPretty.register_uri(HTTPretty.GET, "https://yipit.com/",
                           body="Find the best daily deals")

    request('https://yipit.com?foo=bar&foo=baz&chuck=norris', 'GET')
    expect(HTTPretty.last_request.querystring).to.equal({
        'foo': ['bar', 'baz'],
        'chuck': ['norris'],
    })


@httprettified
@within(ten=microseconds)
def test_httpretty_should_mock_headers_pyopenssl(now):
    "HTTPretty should mock basic headers with pyopenssl"

    HTTPretty.register_uri(HTTPretty.GET, "https://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    headers, _ = request('https://github.com', 'GET')
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
@within(ten=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_pyopenssl(now):
    "HTTPretty should allow adding and overwritting headers with pyopenssl"

    HTTPretty.register_uri(HTTPretty.GET, "https://github.com/foo",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '27',
                               'Content-Type': 'application/json',
                           })

    headers, _ = request('https://github.com/foo', 'GET')

    expect(dict(headers)).to.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(ten=microseconds)
def test_httpretty_should_allow_forcing_headers_pyopenssl(now):
    "HTTPretty should allow forcing headers with pyopenssl"

    HTTPretty.register_uri(HTTPretty.GET, "https://github.com/foo",
                           body="this is supposed to be the response",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                           })

    headers, _ = request('https://github.com/foo', 'GET')

    expect(dict(headers)).to.equal({
        'content-type': 'application/xml',
        'status': '200',
    })


@httprettified
@within(ten=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2(now):
    "HTTPretty should allow adding and overwritting headers by keyword args " \
        "with pyopenssl"

    HTTPretty.register_uri(HTTPretty.GET, "https://github.com/foo",
                           body="this is supposed to be the response",
                           server='Apache',
                           content_length='27',
                           content_type='application/json')

    headers, _ = request('https://github.com/foo', 'GET')

    expect(dict(headers)).to.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(ten=microseconds)
def test_rotating_responses_with_pyopenssl(now):
    "HTTPretty should support rotating responses with pyopenssl"

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        responses=[
            HTTPretty.Response(body="first response", status=201),
            HTTPretty.Response(body='second and last response', status=202),
        ])

    headers1, body1 = request(
        'https://api.yahoo.com/test', 'GET')

    expect(headers1['status']).to.equal('201')
    expect(body1).to.equal(b'first response')

    headers2, body2 = request(
        'https://api.yahoo.com/test', 'GET')

    expect(headers2['status']).to.equal('202')
    expect(body2).to.equal(b'second and last response')

    headers3, body3 = request(
        'https://api.yahoo.com/test', 'GET')

    expect(headers3['status']).to.equal('202')
    expect(body3).to.equal(b'second and last response')


@httprettified
@within(ten=microseconds)
def test_can_inspect_last_request(now):
    "HTTPretty.last_request is a mimetools.Message request from last match"

    HTTPretty.register_uri(HTTPretty.POST, "https://api.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    headers, body = request(
        'https://api.github.com', 'POST',
        body='{"username": "gabrielfalcao"}',
        headers={
            'content-type': 'text/json',
        },
    )

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        b'{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(body).to.equal(b'{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(ten=microseconds)
def test_can_inspect_last_request_with_ssl(now):
    "HTTPretty.last_request is recorded even when mocking 'https' (SSL)"

    HTTPretty.register_uri(HTTPretty.POST, "https://secure.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    headers, body = request(
        'https://secure.github.com', 'POST',
        body='{"username": "gabrielfalcao"}',
        headers={
            'content-type': 'text/json',
        },
    )

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        b'{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(body).to.equal(b'{"repositories": ["HTTPretty", "lettuce"]}')


@httprettified
@within(ten=microseconds)
def test_httpretty_ignores_querystrings_from_registered_uri(now):
    "Registering URIs with query string cause them to be ignored"

    HTTPretty.register_uri(HTTPretty.GET, "https://yipit.com/?id=123",
                           body="Find the best daily deals")

    _, got = request('https://yipit.com/?id=123', 'GET')

    expect(got).to.equal(b'Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/?id=123')


@httprettified
@within(ten=microseconds)
def test_callback_response(now):
    ("HTTPretty should all a callback function to be set as the body with"
      " pyopenssl")

    def request_callback(request, uri, headers):
        return [200,headers,"The {0} response from {1}".format(decode_utf8(request.method), uri)]

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        body=request_callback)

    headers1, body1 = request(
        'https://api.yahoo.com/test', 'GET')

    expect(body1).to.equal(b"The GET response from https://api.yahoo.com/test")

    HTTPretty.register_uri(
        HTTPretty.POST, "https://api.yahoo.com/test_post",
        body=request_callback)

    headers2, body2 = request(
        'https://api.yahoo.com/test_post', 'POST')

    expect(body2).to.equal(b"The POST response from https://api.yahoo.com/test_post")


@httprettified
def test_httpretty_should_allow_registering_regexes():
    "HTTPretty should allow registering regexes with pyopenssl"

    HTTPretty.register_uri(
        HTTPretty.GET,
        re.compile("https://api.yipit.com/v1/deal;brand=(?P<brand_name>\w+)"),
        body="Found brand",
    )

    response, body = request('https://api.yipit.com/v1/deal;brand=gap', 'GET')
    expect(body).to.equal(b'Found brand')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/v1/deal;brand=gap')

