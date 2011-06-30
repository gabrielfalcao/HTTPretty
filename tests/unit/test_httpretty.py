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

from sure import that
from httpretty import HTTPretty, HTTPrettyError


def test_httpretty_should_raise_proper_exception_on_inconsistent_length():
    u"HTTPretty should raise proper exception on inconsistent Content-Length / "\
    "registered response body"
    assert that(
        HTTPretty.register_uri,
        with_args=(
            HTTPretty.GET, "http://github.com/gabrielfalcao"
        ),
        and_kwargs=dict(
            body="that's me!",
            adding_headers={
                'Content-Length': '999'
            }
        )
    ).raises(
        HTTPrettyError,
        'HTTPretty got inconsistent parameters. The header Content-Length you registered expects size "999" '
        'but the body you registered for that has actually length "10".\n'
        'Fix that, or if you really want that, call register_uri with "fill_with" callback.'
    )


def test_does_not_have_last_request_by_default():
    u'HTTPretty.last_request is a dummy object by default'

    assert that(HTTPretty.last_request.headers).is_empty
    assert that(HTTPretty.last_request.body).is_empty
