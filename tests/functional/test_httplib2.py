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
import httplib2
from sure import *
from httpretty import HTTPretty

def enable_httpretty(context):
    HTTPretty.enable()

@that_with_context(enable_httpretty)
@within(two=microseconds)
def test_httpretty_should_mock_a_simple_get_with_httplib2_read():
    u"HTTPretty should mock a simple GET with httplib2.Http()"

    HTTPretty.register_uri(HTTPretty.GET, "http://globo.com/",
                           body="The biggest portal in Brazil")

    http = httplib2.Http()
    (_, got) = http.request('http://globo.com', 'GET')
    assert that(got).equals('The biggest portal in Brazil')
