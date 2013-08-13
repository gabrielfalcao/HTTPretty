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

import json
import requests
from sure import expect, within, microseconds
from contextlib import contextmanager

import httpretty
from httpretty.compat import StringIO

try:
    import mock as pypimock
    mock = pypimock
except ImportError:
    import unittest
    mock = unittest.mock


@within(two=microseconds)
def test_httpretty_recording_writes_file(now):
    f = StringIO()
    @contextmanager
    def new_open(*args, **kwargs):
        yield f
    with mock.patch('__builtin__.open', new_open):
        with httpretty.record('somefile.json'):
            httpretty.register_uri(
                httpretty.GET,
                "http://leadsift.com/",
                body="Find leads on social media"
            )
            requests.get('http://leadsift.com/')
    output = json.loads(f.getvalue())
    expect(output['GET|http://leadsift.com/'][0]['body']).should.equal(
        "Find leads on social media"
    )

@within(two=microseconds)
def test_httpretty_record_or_playback_writes_file(now):
    f = StringIO()
    @contextmanager
    def new_open(*args, **kwargs):
        yield f
    with mock.patch('os.path.exists') as exists:
        exists.return_value = False
        with mock.patch('__builtin__.open', new_open):
            with httpretty.record_or_playback('somefile.json'):
                httpretty.register_uri(
                    httpretty.GET,
                    "http://leadsift.com/",
                    body="Find leads on social media"
                )
                requests.get('http://leadsift.com/')
    output = json.loads(f.getvalue())
    expect(output['GET|http://leadsift.com/'][0]['body']).should.equal(
        "Find leads on social media"
    )

@within(two=microseconds)
def test_httpretty_record_or_playback_playback_if_file_exists(now):
    f = StringIO('''{
        "GET|http://leadsift.com/": [{
            "status": 200,
            "forcing_headers": {
                "status": 200,
                "content-length": "26",
                "content-type": "text/plain; charset=utf-8"
            },
            "body": "Find leads on social media"
        }]
    }''')
    f.write = mock.MagicMock()
    @contextmanager
    def new_open(*args, **kwargs):
        yield f
    with mock.patch('os.path.exists') as exists:
        exists.return_value = True
        with mock.patch('__builtin__.open', new_open):
            with httpretty.record_or_playback('somefile.json'):
                requests.get('http://leadsift.com/')
    expect(f.write.called).should_not.be.ok
