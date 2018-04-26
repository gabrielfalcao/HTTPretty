# #!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

import io
import types

from six import PY3, text_type, string_types, binary_type

if PY3:  # pragma: no cover
    StringIO = io.BytesIO
    basestring = string_types

else:  # pragma: no cover
    import StringIO
    StringIO = StringIO.StringIO
    basestring = string_types


class BaseClass(object):

    def __repr__(self):
        ret = self.__str__()
        if PY3:  # pragma: no cover
            return ret
        else:
            return ret.encode('utf-8')


try:  # pragma: no cover
    from urllib.parse import urlsplit
    from urllib.parse import urlunsplit
    from urllib.parse import parse_qs
    from urllib.parse import quote
    from urllib.parse import quote_plus
    from urllib.parse import unquote
    unquote_utf8 = unquote
except ImportError:  # pragma: no cover
    from urlparse import urlsplit, urlunsplit, parse_qs, unquote
    from urllib import quote, quote_plus

    def unquote_utf8(qs):
        if isinstance(qs, text_type):
            qs = qs.encode('utf-8')
        s = unquote(qs)
        if isinstance(s, binary_type):
            return s.decode('utf-8', errors='ignore')
        else:
            return s


try:  # pragma: no cover
    from http.server import BaseHTTPRequestHandler
except ImportError:  # pragma: no cover
    from BaseHTTPServer import BaseHTTPRequestHandler


ClassTypes = (type,)
if not PY3:  # pragma: no cover
    ClassTypes = (type, types.ClassType)


__all__ = [
    'PY3',
    'StringIO',
    'text_type',
    'binary_type',
    'BaseClass',
    'BaseHTTPRequestHandler',
    'quote',
    'quote_plus',
    'urlunsplit',
    'urlsplit',
    'parse_qs',
    'ClassTypes',
]
