# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2021> Gabriel Falcão <gabriel@nacaolivre.org>
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
import socket
from unittest import skip
from sure import scenario, expect
from httpretty import httprettified


def create_socket(context):
    context.sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP,
    )
    context.sock.is_http = True


@skip('not currently supported')
@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_send(context=None):
    "HTTPretty should forward_and_trace socket.send"

    expect(context.sock.send).when.called_with(b'data').to.throw(
        "not connected"
    )


@skip('not currently supported')
@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_sendto(context=None):
    "HTTPretty should forward_and_trace socket.sendto"

    expect(context.sock.sendto).when.called.to.throw(
        "not connected"
    )


@skip('not currently supported')
@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_recvfrom(context=None):
    "HTTPretty should forward_and_trace socket.recvfrom"

    expect(context.sock.recvfrom).when.called.to.throw(
        "not connected"
    )


@skip('not currently supported')
@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_recv_into(context=None):
    "HTTPretty should forward_and_trace socket.recv_into"
    buf = bytearray()
    expect(context.sock.recv_into).when.called_with(buf).to.throw(
        "not connected"
    )


@skip('not currently supported')
@httprettified
@scenario(create_socket)
def test_httpretty_debugs_socket_recvfrom_into(context=None):
    "HTTPretty should forward_and_trace socket.recvfrom_into"

    expect(context.sock.recvfrom_into).when.called.to.throw(
        "not connected"
    )
