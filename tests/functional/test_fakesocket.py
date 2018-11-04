# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2018>  Gabriel Falcão <gabriel@nacaolivre.org>
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

import functools
import socket

import mock


class FakeSocket(socket.socket):
    """
    Just an editable socket factory
    It allows mock to patch readonly functions
    """

    connect = sendall = lambda *args, **kw: None


fake_socket_interupter_flag = {}


def recv(flag, size):
    """
    Two pass recv implementation

    This implementation will for the first time send something that is smaller than
    the asked size passed in argument.
    Any further call will just raise RuntimeError
    """
    if "was_here" in flag:
        raise RuntimeError("Already sent everything")
    else:
        flag["was_here"] = None
        return "a" * (size - 1)


recv = functools.partial(recv, fake_socket_interupter_flag)


@mock.patch("httpretty.old_socket", new=FakeSocket)
def _test_shorten_response():
    u"HTTPretty shouldn't try to read from server when communication is over"
    from sure import expect
    import httpretty

    fakesocket = httpretty.fakesock.socket(socket.AF_INET, socket.SOCK_STREAM)
    with mock.patch.object(fakesocket.truesock, "recv", recv):
        fakesocket.connect(("localhost", 80))
        fakesocket._true_sendall("WHATEVER")
        expect(fakesocket.fd.read()).to.equal("a" * (httpretty.socket_buffer_size - 1))
