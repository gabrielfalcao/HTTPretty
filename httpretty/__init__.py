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
import re
import socket

from datetime import datetime
from StringIO import StringIO
from urlparse import urlsplit

class fakesock(object):
    old_socket = socket.socket

    class socket(object):
        _entry = None
        def __init__(self, family, type, protocol):
            self.family = family
            self.type = type
            self.protocol = protocol

        def connect(self, address):
            self._address = (self._host, self._port) = address
            self._closed = False

        def close(self):
            self._closed = True

        def makefile(self, mode, bufsize):
            self._mode = mode
            self._bufsize = bufsize
            fd = StringIO()

            if self._entry:
                self._entry.fill_filekind(fd)

            return fd

        def sendall(self, data):
            verb, headers_string = data.split('\n', 1)
            method, path, version = re.split('\s+', verb.strip(), 3)

            info = URIInfo(hostname=self._host, port=self._port, path=path)

            entry = HTTPretty._entries.get(info, None)
            if not entry:
                return

            if entry.method == method:
                self._entry = entry

def create_fake_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    s = fakesock.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
        s.settimeout(timeout)

    s.connect(address)
    return s

STATUSES = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Time-out",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Large",
    415: "Unsupported Media Type",
    416: "Requested range not satisfiable",
    417: "Expectation Failed",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Time-out",
    505: "HTTP Version not supported",
}

class Entry(object):
    def __init__(self, method, uri, body):
        self.method = method
        self.uri = uri
        self.body = body

    def fill_filekind(self, fk):
        now = datetime.utcnow()
        headers = {
            'Status': 200,
            'Date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Server': 'Python/HTTPretty',
            'Connection': 'close',
        }
        status = headers['Status']

        string_list = [
            'HTTP/1.1 %d %s' % (status, STATUSES[status]),
            'Date: %s' % headers.pop('Date'),
            'Content-Type: %s' % headers.pop('Content-Type', 'text/plain; charset=utf-8'),
            'Content-Length: %s' % headers.pop('Content-Length', len(self.body)),
            'Server: %s' % headers.pop('Server'),
        ]
        for k, v in headers.items():
            string_list.append(
                '%s: %s' % (k, unicode(v))
            )

        fk.write("\n".join(string_list))
        fk.write('\n\r\n')
        fk.write(self.body)
        fk.seek(0)

class URIInfo(object):
    def __init__(self, username='', password='', hostname='', port=80, path='/', query='', fragment=''):
        self.username = username or ''
        self.password = password or ''
        self.hostname = hostname or ''
        self.port = int(port) != 80 and str(port) or ''
        self.path = path or ''
        self.query = query or ''
        self.fragment = fragment or ''

    def __unicode__(self):
        attrs = 'username', 'password', 'hostname', 'port', 'path', 'query', 'fragment'
        return ur'<httpretty.URIInfo(%s)>' % ", ".join(['%s="%s"' % (k, getattr(self, k, '')) for k in attrs])

    def __repr__(self):
        return unicode(self)

    def __hash__(self):
        return hash(unicode(self))

    def __eq__(self, other):
        return unicode(self) == unicode(other)

    @classmethod
    def from_uri(cls, uri):
        result = urlsplit(uri)
        return cls(result.username,
                   result.password,
                   result.hostname,
                   result.port or 80,
                   result.path,
                   result.query,
                   result.fragment)


class HTTPretty(object):
    u"""The URI registration class"""
    _entries = {}

    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    HEAD = 'HEAD'

    @classmethod
    def register_uri(self, method, uri, body):
        self._entries[URIInfo.from_uri(uri)] = Entry(method, uri, body)

    def __repr__(self):
        return u'<HTTPretty with %d URI entries>' % len(self._entries)

socket.socket = fakesock.socket
socket.create_connection = create_fake_connection
socket.create = fakesock.socket
socket.__dict__.update(fakesock.__dict__)
