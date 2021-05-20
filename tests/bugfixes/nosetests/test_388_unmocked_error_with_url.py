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
import requests
import httpretty
from httpretty.errors import UnmockedError

from unittest import skip
from sure import expect


def http():
    sess = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1)
    sess.mount('http://', adapter)
    sess.mount('https://', adapter)
    return sess

@httpretty.activate(allow_net_connect=False)
def test_https_forwarding():
    "#388 UnmockedError is raised with details about the mismatched request"
    httpretty.register_uri(httpretty.GET, 'http://google.com/', body="Not Google")
    httpretty.register_uri(httpretty.GET, 'https://google.com/', body="Not Google")
    response1 = http().get('http://google.com/')
    response2 = http().get('https://google.com/')

    http().get.when.called_with("https://github.com/gabrielfalcao/HTTPretty").should.have.raised(UnmockedError, 'https://github.com/gabrielfalcao/HTTPretty')

    response1.text.should.equal(response2.text)
    try:
        http().get("https://github.com/gabrielfalcao/HTTPretty")
    except UnmockedError as exc:
        expect(exc).to.have.property('request')
        expect(exc.request).to.have.property('host').being.equal('github.com')
        expect(exc.request).to.have.property('protocol').being.equal('https')
        expect(exc.request).to.have.property('url').being.equal('https://github.com/gabrielfalcao/HTTPretty')
