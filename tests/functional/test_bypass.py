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
    import urllib.request as urllib2
except ImportError:
    import urllib2

from .testserver import TornadoServer, TCPServer, TCPClient
from sure import expect, that_with_context
from httpretty import HTTPretty, httprettified


def start_http_server(context):
    context.server = TornadoServer(9999)
    context.server.start()
    HTTPretty.enable()


def stop_http_server(context):
    context.server.stop()
    HTTPretty.enable()


def start_tcp_server(context):
    context.server = TCPServer(8888)
    context.server.start()
    context.client = TCPClient(8888)
    HTTPretty.enable()


def stop_tcp_server(context):
    context.server.stop()
    context.client.close()
    HTTPretty.enable()


@httprettified
@that_with_context(start_http_server, stop_http_server)
def test_httpretty_bypasses_when_disabled(context):
    u"HTTPretty should bypass all requests by disabling it"

    HTTPretty.register_uri(
        HTTPretty.GET, "http://localhost:9999/go-for-bubbles/",
        body="glub glub")

    HTTPretty.disable()

    fd = urllib2.urlopen('http://localhost:9999/go-for-bubbles/')
    got1 = fd.read()
    fd.close()

    expect(got1).to.equal(
        b'. o O 0 O o . o O 0 O o . o O 0 O o . o O 0 O o . o O 0 O o .')

    fd = urllib2.urlopen('http://localhost:9999/come-again/')
    got2 = fd.read()
    fd.close()

    expect(got2).to.equal(b'<- HELLO WORLD ->')

    HTTPretty.enable()

    fd = urllib2.urlopen('http://localhost:9999/go-for-bubbles/')
    got3 = fd.read()
    fd.close()

    expect(got3).to.equal(b'glub glub')


@httprettified
@that_with_context(start_http_server, stop_http_server)
def test_httpretty_bypasses_a_unregistered_request(context):
    u"HTTPretty should bypass a unregistered request by disabling it"

    HTTPretty.register_uri(
        HTTPretty.GET, "http://localhost:9999/go-for-bubbles/",
        body="glub glub")

    fd = urllib2.urlopen('http://localhost:9999/go-for-bubbles/')
    got1 = fd.read()
    fd.close()

    expect(got1).to.equal(b'glub glub')

    fd = urllib2.urlopen('http://localhost:9999/come-again/')
    got2 = fd.read()
    fd.close()

    expect(got2).to.equal(b'<- HELLO WORLD ->')


@httprettified
@that_with_context(start_tcp_server, stop_tcp_server)
def test_using_httpretty_with_other_tcp_protocols(context):
    u"HTTPretty should work even when testing code that also use other TCP-based protocols"

    HTTPretty.register_uri(
        HTTPretty.GET, "http://falcao.it/foo/",
        body="BAR")

    fd = urllib2.urlopen('http://falcao.it/foo/')
    got1 = fd.read()
    fd.close()

    expect(got1).to.equal(b'BAR')

    expect(context.client.send("foobar")).to.equal("RECEIVED: foobar")
