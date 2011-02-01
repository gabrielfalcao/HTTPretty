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
import urllib2
from testserver import Server
from sure import that, that_with_context
from httpretty import HTTPretty

def start_server(context):
    context.server = Server(9999)
    context.server.start()
    HTTPretty.enable()

def stop_server(context):
    context.server.stop()
    HTTPretty.enable()

@that_with_context(start_server, stop_server)
def test_httpretty_bypasses_a_unregistered_request():
    u"HTTPretty should bypass a unregistered request by disabling it"

    HTTPretty.register_uri(HTTPretty.GET, "http://localhost:9999/go-for-bubbles/",
                           body="glub glub")

    fd = urllib2.urlopen('http://localhost:9999/go-for-bubbles/')
    got1 = fd.read()
    fd.close()

    assert that(got1).equals('glub glub')

    HTTPretty.disable()

    fd = urllib2.urlopen('http://localhost:9999/come-again/')
    got2 = fd.read()
    fd.close()

    assert that(got2).equals('<- HELLO WORLD ->')


