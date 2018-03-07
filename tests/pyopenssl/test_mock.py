# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2015>  Gabriel Falcão <gabriel@nacaolivre.org>
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

import requests

from httpretty import HTTPretty, httprettified
from sure import expect

from requests.packages.urllib3.contrib.pyopenssl import inject_into_urllib3, extract_from_urllib3


@httprettified
def test_httpretty_overrides_when_pyopenssl_installed():
    ('HTTPretty should remove PyOpenSSLs urllib3 mock if it is installed')

    # When we run Httpretty with PyOpenSSL and ndg-httpsclient installed
    from httpretty.core import pyopenssl_override

    # Then we override pyopenssl
    pyopenssl_override.should.be.true

    # And HTTPretty works successfully
    HTTPretty.register_uri(HTTPretty.GET, "https://yipit.com/",
                           body="Find the best daily deals")

    response = requests.get('https://yipit.com')
    expect(response.text).to.equal('Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/')


@httprettified
def test_httpretty_fails_when_pyopenssl_is_not_replaced():
    ('HTTPretty should fail if PyOpenSSL is installed and we do not remove the monkey patch')

    # When we don't replace the PyOpenSSL monkeypatch
    inject_into_urllib3()

    # And we use HTTPretty on as ssl site
    HTTPretty.register_uri(HTTPretty.GET, "https://yipit.com/",
                           body="Find the best daily deals")

    # Then we get an SSL error
    requests.get.when.called_with('https://yipit.com').should.throw(requests.exceptions.SSLError)

    # Undo injection after test
    extract_from_urllib3()