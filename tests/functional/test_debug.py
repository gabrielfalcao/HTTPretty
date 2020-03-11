# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2020> Gabriel Falcão <gabriel@nacaolivre.org>
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
import socket
from sure import scenario, expect
from httpretty import httprettified


def create_socket(context):
    context.sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP,
    )
    context.sock.is_http = True


@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_send(context):
    "HTTPretty should forward_and_trace socket.send"

    expect(context.sock.send).when.called.to.throw(
        AssertionError,
        "not connected"
    )


@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_sendto(context):
    "HTTPretty should forward_and_trace socket.sendto"

    expect(context.sock.sendto).when.called.to.throw(
        AssertionError,
        "not connected"
    )


@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_recv(context):
    "HTTPretty should forward_and_trace socket.recv"

    expect(context.sock.recv).when.called.to.throw(
        AssertionError,
        "not connected"
    )


@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_recvfrom(context):
    "HTTPretty should forward_and_trace socket.recvfrom"

    expect(context.sock.recvfrom).when.called.to.throw(
        AssertionError,
        "not connected"
    )


@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_recv_into(context):
    "HTTPretty should forward_and_trace socket.recv_into"

    expect(context.sock.recv_into).when.called.to.throw(
        AssertionError,
        "not connected"
    )


@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_recvfrom_into(context):
    "HTTPretty should forward_and_trace socket.recvfrom_into"

    expect(context.sock.recvfrom_into).when.called.to.throw(
        AssertionError,
        "not connected"
    )
