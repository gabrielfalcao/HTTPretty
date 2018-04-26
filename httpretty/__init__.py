# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2018>  Gabriel Falcao <gabriel@nacaolivre.org>
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

from .core import httpretty
from .core import httprettified
from .core import EmptyRequestHeaders
from .core import HTTPrettyRequestEmpty  # noqa
from .core import URIInfo
from .errors import HTTPrettyError, UnmockedError
from .version import version

__version__ = version

HTTPretty = httpretty
activate = httprettified

enable = httpretty.enable
register_uri = httpretty.register_uri
disable = httpretty.disable
is_enabled = httpretty.is_enabled
reset = httpretty.reset
Response = httpretty.Response

GET = httpretty.GET
PUT = httpretty.PUT
POST = httpretty.POST
DELETE = httpretty.DELETE
HEAD = httpretty.HEAD
PATCH = httpretty.PATCH
OPTIONS = httpretty.OPTIONS
CONNECT = httpretty.CONNECT


def last_request():
    """returns the last request"""
    return httpretty.last_request


def has_request():
    """returns a boolean indicating whether any request has been made"""
    return not isinstance(httpretty.last_request.headers, EmptyRequestHeaders)


__all__ = [
    'last_request',
    'has_request',
    'GET',
    'PUT',
    'POST',
    'DELETE',
    'HEAD',
    'PATCH',
    'OPTIONS',
    'CONNECT',
    'register_uri',
    'enable',
    'disable',
    'is_enabled',
    'reset',
    'Response',
    'URIInfo',
    'UnmockedError',
    'HTTPrettyError',
    'httpretty',
    'httprettified',
    'EmptyRequestHeaders',
]
