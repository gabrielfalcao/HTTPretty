# HTTPretty
> Version 0.5.2

[![Build Status](https://secure.travis-ci.org/gabrielfalcao/HTTPretty.png)](http://travis-ci.org/gabrielfalcao/HTTPretty)

# In a nutshell

Once upon a time a python developer wanted to use a RESTful api,
everything was fine but until the day he needed to test the code that
hits the RESTful API: what if the API server is down? What if its
content has changed ?

Don't worry, HTTPretty is here for you:

```python
import requests
from sure import expect
from httpretty import HTTPretty
from httpretty import httprettified


@httprettified
def test_yipit_api_returning_deals():
    HTTPretty.register_uri(HTTPretty.GET, "http://api.yipit.com/v1/deals/",
                           body='[{"title": "Test Deal"}]',
                           content_type="application/json")

    response = requests.get('http://api.yipit.com/v1/deals/')

    expect(response.json).to.equal([{"title": "Test Deal"}])
```

# A more technical description

HTTPretty is a HTTP client mock library for Python 100% inspired on ruby's [FakeWeb](http://fakeweb.rubyforge.org/).
If you come from ruby this would probably sound familiar :smiley:

# Usage

## expecting a simple response body

```python
import requests
from httpretty import HTTPretty

def test_one():
    HTTPretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    response = requests.get('http://yipit.com')

    assert response.text == "Find the best daily deals"

    HTTPretty.disable()  # disable afterwards, so that you will have no problems in coda that uses that socket module
```

## ohhhh, really? can that be easier?

**YES** we've got a decorator

```python
import requests
from httpretty import HTTPretty, httprettified

@httprettified
def test_one():
    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    response = requests.get('http://yipit.com')
    assert response.text == "Find the best daily deals"
```

the `@httprettified` is a short-hand decorator that wraps the
decorated function with HTTPretty.enable() and then calls
HTTPretty.disable() right after.

## mocking the status code

```python
import requests
from sure import expect
from httpretty import HTTPretty, httprettified

@httprettified
def test_github_access():
    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="here is the mocked body",
                           status=201)

    response = requests.get('http://github.com')
    expect(response.status_code).to.equal(201)
```

## you can tell HTTPretty to return any HTTP headers you want

**and all you need is to add keyword args in which the keys are always lower-cased and with underscores `_` instead of dashes `-`**

For example, let's say you want to mock that server returns `content-type`.
To do so, use the argument `content_type`, **all the keyword args are taken by HTTPretty and transformed in the RFC2616 equivalent name**.

```python
@httprettified
def test_some_api():
    HTTPretty.register_uri(HTTPretty.GET, "http://foo-api.com/gabrielfalcao",
                           body='{"success": false}',
                           status=500,
                           content_type='text/json')

    response = requests.get('http://foo-api.com/gabrielfalcao')

    expect(response.json).to.equal({'success': False})
    expect(response.status_code).to.equal(500)
```

## rotating responses

same URL, same request method, the first request return the first
HTTPretty.Response, all the subsequent ones return the last (status 202)

```python
import requests
from sure import expect


@httprettified
def test_rotating_responses():
    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/gabrielfalcao/httpretty",
                           responses=[
                               HTTPretty.Response(body="first response", status=201),
                               HTTPretty.Response(body='second and last response', status=202),
                            ])

    response1 = requests.get('http://github.com/gabrielfalcao/httpretty')
    expect(response1.status_code).to.equal(201)
    expect(response1.text).to.equal('first response')

    response2 = requests.get('http://github.com/gabrielfalcao/httpretty')
    expect(response2.status_code).to.equal(202)
    expect(response2.text).to.equal('second and last response')

    response3 = requests.get('http://github.com/gabrielfalcao/httpretty')

    expect(response3.status_code).to.equal(202)
    expect(response3.text).to.equal('second and last response')
```

## expect for a response, and check the request got by the "server" to make sure it was fine.

```python
import requests
from sure import expect
from httpretty import HTTPretty, httprettified


@httprettified
def test_yipit_api_integration():
    HTTPretty.register_uri(HTTPretty.POST, "http://api.yipit.com/foo/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    response = requests.post('http://api.yipit.com/foo',
                            '{"username": "gabrielfalcao"}',
                            headers={
                                'content-type': 'text/json',
                            })

    expect(response.text).to.equal('{"repositories": ["HTTPretty", "lettuce"]}')
    expect(HTTPretty.last_request.method).to.equal("POST")
    expect(HTTPretty.last_request.headers['content-type']).to.equal('text/json')
```

# Motivation

When building systems that access external resources such as RESTful
webservices, XMLRPC or even simple HTTP requests, we stumble in the
problem:

    "I'm gonna need to mock all those requests"

It brings a lot of hassle, you will need to use a generic mocking
tool, mess with scope and so on.

## The idea behind HTTPretty (how it works)

HTTPretty [monkey patches](http://en.wikipedia.org/wiki/Monkey_patch)
Python's [socket](http://docs.python.org/library/socket.html) core
module, reimplementing the HTTP protocol, by mocking requests and
responses.

As for it works in this way, you don't need to worry what http library
you're gonna use.

HTTPretty will mock the response for you :) *(and also give you the latest requests so that you can check them)*

# Acknowledgements

## caveats with the [requests](http://docs.python-requests.org/en/latest/) library

### `forcing_headers` + `Content-Length`

if you use the `forcing_headers` options make sure to add the header
`Content-Length` otherwise the
[requests](http://docs.python-requests.org/en/latest/) will try to
load the response endlessly

# Officially supported libraries

Because HTTPretty works in the socket level it should work with any HTTP client libraries, although it is [battle tested](https://github.com/gabrielfalcao/HTTPretty/tree/master/tests/functional) against:

* [requests](http://docs.python-requests.org/en/latest/)
* [httplib2](http://code.google.com/p/httplib2/)
* [urllib2](http://docs.python.org/2/library/urllib2.html)

# Hacking on HTTPretty

#### create a virtual env

you will need [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/)


```console
mkvirtualenv --distribute --no-site-packages HTTPretty
```

#### install the dependencies

```console
pip install -r requirements.pip
```

#### next steps:

1. run the tests with make:
```bash
make unit functional
```
2. hack at will
3. commit, push etc
4. send a pull request

# License

    <HTTPretty - HTTP client mock for Python>
    Copyright (C) <2011-2012>  Gabriel Falcão <gabriel@nacaolivre.org>

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
