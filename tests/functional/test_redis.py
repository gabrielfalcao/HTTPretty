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

import redis
import socket
import requests
from sure import expect
from httpretty import HTTPretty

try:
    xrange = xrange
except NameError:
    xrange = range

try:
    advance_iterator = next
except NameError:
    def advance_iterator(it):
        return it.next()
next = advance_iterator


def test_redis_and_requests():

    # first let's create a redis connection, for real

    redis_conn = redis.Redis()

    # let's enable HTTPretty

    HTTPretty.enable()

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    retrieved_keys = redis_conn.keys("*")
    response = requests.get('http://yipit.com')
    expect(response.text).to.equal('Find the best daily deals')
    expect(redis_conn.connection_pool._available_connections[0]._sock).to.be.a(socket._socketobject)
