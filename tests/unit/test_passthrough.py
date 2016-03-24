# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
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

def test_http_passthrough():
    from sure import expect
    from httpretty import HTTPretty
    import requests
    
    url = 'http://checkip.dyndns.com/'
    
    response1 = requests.get(url)
    
    HTTPretty.enable()
    HTTPretty.register_uri(HTTPretty.GET, 'http://google.com/', body="Not Google")
    
    response2 = requests.get('http://google.com/')
    expect(response2.content).to.equal('Not Google')
    
    response3 = requests.get(url)
    expect(response3.content).to.equal(response1.content)
    
    HTTPretty.disable()
    
    response4 = requests.get(url)
    expect(response4.content).to.equal(response1.content)
    
def test_https_passthrough():
    from sure import expect
    from httpretty import HTTPretty
    import requests
    
    url = 'https://www.cloudflare.com/ips-v4'
    
    response1 = requests.get(url)
    
    HTTPretty.enable()
    HTTPretty.register_uri(HTTPretty.GET, 'http://google.com/', body="Not Google")
    
    response2 = requests.get('http://google.com/')
    expect(response2.content).to.equal('Not Google')
    
    response3 = requests.get(url)
    expect(response3.content).to.equal(response1.content)
    
    HTTPretty.disable()
    
    response4 = requests.get(url)
    expect(response4.content).to.equal(response1.content)
