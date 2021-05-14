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

from sure import expect


def http():
    sess = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1)
    sess.mount('http://', adapter)
    sess.mount('https://', adapter)
    return sess


def test_http_passthrough():
    url = 'http://httpbin.org/status/200'
    response1 = http().get(url)

    response1 = http().get(url)

    httpretty.enable(allow_net_connect=False, verbose=True)
    httpretty.register_uri(httpretty.GET, 'http://google.com/', body="Not Google")
    httpretty.register_uri(httpretty.GET, url, body="mocked")

    response2 = http().get('http://google.com/')
    expect(response2.content).to.equal(b'Not Google')

    response3 = http().get(url)
    response3.content.should.equal(b"mocked")

    httpretty.disable()

    response4 = http().get(url)
    (response4.content).should.equal(response1.content)


def test_https_passthrough():
    url = 'https://httpbin.org/status/200'

    response1 = http().get(url)

    httpretty.enable(allow_net_connect=False, verbose=True)
    httpretty.register_uri(httpretty.GET, 'https://google.com/', body="Not Google")
    httpretty.register_uri(httpretty.GET, url, body="mocked")

    response2 = http().get('https://google.com/')
    expect(response2.content).to.equal(b'Not Google')

    response3 = http().get(url)
    (response3.text).should.equal('mocked')

    httpretty.disable()

    response4 = http().get(url)
    (response4.content).should.equal(response1.content)
