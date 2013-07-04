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
from sure import expect
from httpretty import HTTPretty, HTTPrettyError
from httpretty.core import URIInfo, BaseClass, Entry, FakeSockFile
from httpretty.http import STATUSES

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock


def test_httpretty_should_raise_proper_exception_on_inconsistent_length():
    "HTTPretty should raise proper exception on inconsistent Content-Length / "\
       "registered response body"
    expect(HTTPretty.register_uri).when.called_with(
      HTTPretty.GET,
        "http://github.com/gabrielfalcao",
        body="that's me!",
        adding_headers={
            'Content-Length': '999'
        }
    ).to.throw(
        HTTPrettyError,
        'HTTPretty got inconsistent parameters. The header Content-Length you registered expects size "999" '
        'but the body you registered for that has actually length "10".'
    )


def test_does_not_have_last_request_by_default():
    'HTTPretty.last_request is a dummy object by default'
    HTTPretty.reset()

    expect(HTTPretty.last_request.headers).to.be.empty
    expect(HTTPretty.last_request.body).to.be.empty


def test_status_codes():
    "HTTPretty supports N status codes"

    expect(STATUSES).to.equal({
        100: "Continue",
        101: "Switching Protocols",
        102: "Processing",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        207: "Multi-Status",
        208: "Already Reported",
        226: "IM Used",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        306: "Switch Proxy",
        307: "Temporary Redirect",
        308: "Permanent Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request a Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Request Entity Too Large",
        414: "Request-URI Too Long",
        415: "Unsupported Media Type",
        416: "Requested Range Not Satisfiable",
        417: "Expectation Failed",
        418: "I'm a teapot",
        420: "Enhance Your Calm",
        422: "Unprocessable Entity",
        423: "Locked",
        424: "Failed Dependency",
        424: "Method Failure",
        425: "Unordered Collection",
        426: "Upgrade Required",
        428: "Precondition Required",
        429: "Too Many Requests",
        431: "Request Header Fields Too Large",
        444: "No Response",
        449: "Retry With",
        450: "Blocked by Windows Parental Controls",
        451: "Unavailable For Legal Reasons",
        451: "Redirect",
        494: "Request Header Too Large",
        495: "Cert Error",
        496: "No Cert",
        497: "HTTP to HTTPS",
        499: "Client Closed Request",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
        506: "Variant Also Negotiates",
        507: "Insufficient Storage",
        508: "Loop Detected",
        509: "Bandwidth Limit Exceeded",
        510: "Not Extended",
        511: "Network Authentication Required",
        598: "Network read timeout error",
        599: "Network connect timeout error",
    })


def test_uri_info_full_url():
    uri_info = URIInfo(
        username='johhny',
        password='password',
        hostname=b'google.com',
        port=80,
        path=b'/',
        query=b'foo=bar&baz=test',
        fragment='',
        scheme='',
    )

    expect(uri_info.full_url()).to.equal(
        "http://johhny:password@google.com/?foo=bar&baz=test"
    )

    expect(uri_info.full_url(use_querystring=False)).to.equal(
        "http://johhny:password@google.com/"
    )


def test_global_boolean_enabled():
    expect(HTTPretty.is_enabled()).to.be.falsy
    HTTPretty.enable()
    expect(HTTPretty.is_enabled()).to.be.truthy
    HTTPretty.disable()
    expect(HTTPretty.is_enabled()).to.be.falsy


def test_py3kobject_implements_valid__repr__based_on__str__():
    class MyObject(BaseClass):
        def __str__(self):
            return 'hi'

    myobj = MyObject()
    expect(repr(myobj)).to.be.equal('hi')


def test_Entry_class_normalizes_headers():
    entry = Entry(HTTPretty.GET, 'http://example.com', 'example',
                  host='example.com', cache_control='no-cache', x_forward_for='proxy')

    expect(entry.adding_headers).to.equal({
       'Host':'example.com',
       'Cache-Control':'no-cache',
       'X-Forward-For':'proxy'
    })


def test_Entry_class_counts_multibyte_characters_in_bytes():
    entry = Entry(HTTPretty.GET, 'http://example.com', 'こんにちは')
    buf = FakeSockFile()
    entry.fill_filekind(buf)
    response = buf.getvalue()
    expect(b'content-length: 15\n').to.be.within(response)


def test_fake_socket_passes_through_setblocking():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.setblocking).called_with(0).should_not.throw(AttributeError)
    s.truesock.setblocking.assert_called_with(0)

def test_fake_socket_passes_through_fileno():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.fileno).called_with().should_not.throw(AttributeError)
    s.truesock.fileno.assert_called_with()


def test_fake_socket_passes_through_getsockopt():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.getsockopt).called_with(socket.SOL_SOCKET, 1).should_not.throw(AttributeError)
    s.truesock.getsockopt.assert_called_with(socket.SOL_SOCKET, 1)

def test_fake_socket_passes_through_bind():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.bind).called_with().should_not.throw(AttributeError)
    s.truesock.bind.assert_called_with()

def test_fake_socket_passes_through_connect_ex():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.connect_ex).called_with().should_not.throw(AttributeError)
    s.truesock.connect_ex.assert_called_with()

def test_fake_socket_passes_through_listen():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.listen).called_with().should_not.throw(AttributeError)
    s.truesock.listen.assert_called_with()

def test_fake_socket_passes_through_getpeername():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.getpeername).called_with().should_not.throw(AttributeError)
    s.truesock.getpeername.assert_called_with()

def test_fake_socket_passes_through_getsockname():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.getsockname).called_with().should_not.throw(AttributeError)
    s.truesock.getsockname.assert_called_with()

def test_fake_socket_passes_through_gettimeout():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.gettimeout).called_with().should_not.throw(AttributeError)
    s.truesock.gettimeout.assert_called_with()

def test_fake_socket_passes_through_shutdown():
    import socket
    HTTPretty.enable()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.truesock = MagicMock()
    expect(s.shutdown).called_with(socket.SHUT_RD).should_not.throw(AttributeError)
    s.truesock.shutdown.assert_called_with(socket.SHUT_RD)
