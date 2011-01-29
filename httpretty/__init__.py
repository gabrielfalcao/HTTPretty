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
from urlparse import urlsplit
from StringIO import StringIO

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
                fd.write(self._entry.body.strip())
                fd.seek(0)


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



class Entry(object):
    def __init__(self, method, uri, body):
        self.method = method
        self.uri = uri
        self.body = body

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
