# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <httpretty - HTTP client mock for Python>
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
import time
import requests
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from .testserver import TornadoServer, TCPServer, TCPClient
from .base import get_free_tcp_port
from sure import expect, that_with_context

import functools

import httpretty
from httpretty import core, HTTPretty


def start_http_server(context):
    httpretty.disable()
    context.http_port = get_free_tcp_port()
    context.server = TornadoServer(context.http_port)
    context.server.start()
    ready = False
    timeout = 2
    started_at = time.time()
    while not ready:
        httpretty.disable()
        time.sleep(.1)
        try:
            requests.get('http://localhost:{0}/'.format(context.http_port))
            ready = True
        except:
            if time.time() - started_at >= timeout:
                break

    httpretty.enable()


def stop_http_server(context):
    context.server.stop()
    httpretty.enable()


def start_tcp_server(context):
    context.tcp_port = get_free_tcp_port()
    context.server = TCPServer(context.tcp_port)
    context.server.start()
    context.client = TCPClient(context.tcp_port)
    httpretty.enable()


def stop_tcp_server(context):
    context.server.stop()
    context.client.close()
    httpretty.enable()


@httpretty.activate
@that_with_context(start_http_server, stop_http_server)
def test_httpretty_bypasses_when_disabled(context):
    "httpretty should bypass all requests by disabling it"

    httpretty.register_uri(
        httpretty.GET, "http://localhost:{0}/go-for-bubbles/".format(context.http_port),
        body="glub glub")

    httpretty.disable()

    fd = urllib2.urlopen('http://localhost:{0}/go-for-bubbles/'.format(context.http_port))
    got1 = fd.read()
    fd.close()

    expect(got1).to.equal(
        b'. o O 0 O o . o O 0 O o . o O 0 O o . o O 0 O o . o O 0 O o .')

    fd = urllib2.urlopen('http://localhost:{0}/come-again/'.format(context.http_port))
    got2 = fd.read()
    fd.close()

    expect(got2).to.equal(b'<- HELLO WORLD ->')

    httpretty.enable()

    fd = urllib2.urlopen('http://localhost:{0}/go-for-bubbles/'.format(context.http_port))
    got3 = fd.read()
    fd.close()

    expect(got3).to.equal(b'glub glub')
    core.POTENTIAL_HTTP_PORTS.remove(context.http_port)


@httpretty.activate
@that_with_context(start_http_server, stop_http_server)
def test_httpretty_bypasses_a_unregistered_request(context):
    "httpretty should bypass a unregistered request by disabling it"

    httpretty.register_uri(
        httpretty.GET, "http://localhost:{0}/go-for-bubbles/".format(context.http_port),
        body="glub glub")

    fd = urllib2.urlopen('http://localhost:{0}/go-for-bubbles/'.format(context.http_port))
    got1 = fd.read()
    fd.close()

    expect(got1).to.equal(b'glub glub')

    fd = urllib2.urlopen('http://localhost:{0}/come-again/'.format(context.http_port))
    got2 = fd.read()
    fd.close()

    expect(got2).to.equal(b'<- HELLO WORLD ->')
    core.POTENTIAL_HTTP_PORTS.remove(context.http_port)


@httpretty.activate
@that_with_context(start_tcp_server, stop_tcp_server)
def test_using_httpretty_with_other_tcp_protocols(context):
    "httpretty should work even when testing code that also use other TCP-based protocols"

    httpretty.register_uri(
        httpretty.GET, "http://falcao.it/foo/",
        body="BAR")

    fd = urllib2.urlopen('http://falcao.it/foo/')
    got1 = fd.read()
    fd.close()

    expect(got1).to.equal(b'BAR')

    expect(context.client.send("foobar")).to.equal(b"RECEIVED: foobar")


def disallow_net_connect(test):
    @functools.wraps(test)
    def wrapper(*args, **kwargs):
        HTTPretty.allow_net_connect = False
        try:
            return test(*args, **kwargs)
        finally:
            HTTPretty.allow_net_connect = True
    return wrapper


@disallow_net_connect
@httpretty.activate
@that_with_context(start_http_server, stop_http_server)
def test_disallow_net_connect_1(context):
    """
    When allow_net_connect = False, a request that otherwise
    would have worked results in UnmockedError.
    """
    httpretty.register_uri(httpretty.GET, "http://falcao.it/foo/",
                           body="BAR")

    def foo():
        fd = None
        try:
            fd = urllib2.urlopen('http://localhost:{0}/go-for-bubbles/'.format(context.http_port))
        finally:
            if fd:
                fd.close()

    foo.should.throw(httpretty.UnmockedError)


@disallow_net_connect
@httpretty.activate
def test_disallow_net_connect_2():
    """
    When allow_net_connect = False, a request that would have
    failed results in UnmockedError.
    """

    def foo():
        fd = None
        try:
            fd = urllib2.urlopen('http://example.com/nonsense')
        finally:
            if fd:
                fd.close()

    foo.should.throw(httpretty.UnmockedError)


@disallow_net_connect
@httpretty.activate
def test_disallow_net_connect_3():
    "When allow_net_connect = False, mocked requests still work correctly."

    httpretty.register_uri(httpretty.GET, "http://falcao.it/foo/",
                           body="BAR")
    fd = urllib2.urlopen('http://falcao.it/foo/')
    got1 = fd.read()
    fd.close()
    expect(got1).to.equal(b'BAR')
