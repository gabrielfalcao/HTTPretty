# HTTPretty
> Version 0.3

# What

HTTPretty is a HTTP client mock library for Python 100% inspired on ruby's [FakeWeb](http://fakeweb.rubyforge.org/)

# Motivation

When building systems that access external resources such as RESTful
webservices, XMLRPC or even simple HTTP requests, we stumble in the
problem:

    "I'm gonna need to mock all those requests"

It brings a lot of hassle, you will need to use a generic mocking
tool, mess with scope and so on.

## The idea behind HTTPretty (how it works)

HTTPretty [monkey matches](http://en.wikipedia.org/wiki/Monkey_patch)
Python's [socket](http://docs.python.org/library/socket.html) core
module, reimplementing the HTTP protocol, by mocking requests and
responses.

As for it works in this way, you don't need to worry what http library
you're gonna use.

HTTPretty will mock the response for you :) *(and also give you the latest requests so that you can check them)*

# Usage

## expecting a simple response body

```python
from httpretty import HTTPretty

def test_one():
    HTTPretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
    HTTPretty.register_uri(HTTPretty.GET, "http://globo.com/",
                           body="The biggest portal in Brazil")

    fd = urllib2.urlopen('http://globo.com')
    got = fd.read()
    fd.close()

    assert got == "The biggest portal in Brazil"

    HTTPretty.disable()  # disable afterwards, so that you will have no problems in coda that uses that socket module
```

## ohhhh, really? can that be easier?

**YES** we've got a decorator

```python
from httpretty import HTTPretty, httprettified

@httprettified
def test_one():
    HTTPretty.register_uri(HTTPretty.GET, "http://globo.com/",
                           body="The biggest portal in Brazil")

    fd = urllib2.urlopen('http://globo.com')
    got = fd.read()
    fd.close()

    assert got == "The biggest portal in Brazil"
```

the `@httprettified` is a short-hand decorator that wraps the
decorated function with HTTPretty.enable() and then calls
HTTPretty.disable() right after.

## mocking the status code

```python
from httpretty import HTTPretty, httprettified

@httprettified
def test_github_access():
    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="here is the mocked body",
                           status=201)

    fd = urllib2.urlopen('http://github.com')
    got = fd.read()
    fd.close()

    assert got == "here is the mocked body"
    assert fd.code == 201
```

## you can tell HTTPretty to return any HTTP headers you want

**and all you need is to add keyword args in which the keys are always lower-cased and with underscores `_` instead of dashes `-`**

For example, let's say you want to mock that server returns `content-type`.
To do so, use the argument `content_type`, **all the keyword args are taken by HTTPretty and transformed in the RFC2616 equivalent name**.

```python
HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                       body='{"success": false}',
                       status=500,
                       content_type='text/json')

fd = urllib2.urlopen('http://github.com')
got = fd.read()
fd.close()

assert simplejson.loads(got)['success'] is False
assert fd.code == 500

```


## rotating responses

same URL, same request method, the first request return the first
HTTPretty.Response, all the subsequent ones return the last (status
202)

```python
HTTPretty.register_uri(HTTPretty.GET, "http://github.com/gabrielfalcao/httpretty",
                       responses=[
                           HTTPretty.Response(body="first response", status=201),
                           HTTPretty.Response(body='second and last response', status=202),
                        ])

request1 = urllib2.urlopen('http://github.com/gabrielfalcao/httpretty')
body1 = request1.read()
request1.close()

assert that(request1.code).equals(201)
assert that(body1).equals('first response')

request2 = urllib2.urlopen('http://github.com/gabrielfalcao/httpretty')
body2 = request2.read()
request2.close()
assert that(request2.code).equals(202)
assert that(body2).equals('second and last response')

request3 = urllib2.urlopen('http://github.com/gabrielfalcao/httpretty')
body3 = request3.read()
request3.close()
assert that(request3.code).equals(202)
assert that(body3).equals('second and last response')
```

## expect for a response, and check the request got by the "server" to make sure it was fine.

```python
from httpretty import HTTPretty
from httplib2 import Http

HTTPretty.register_uri(HTTPretty.PATCH, "http://api.github.com/",
                       body='{"repositories": ["HTTPretty", "lettuce"]}')

client = Http()
headers, body = client.request('http://api.github.com', 'PATCH',
                               body='{"username": "gabrielfalcao"}',
                               headers={
                                   'content-type': 'text/json',
                               })
assert body == '{"repositories": ["HTTPretty", "lettuce"]}'
assert HTTPretty.last_request.method == 'PATCH'
assert HTTPretty.last_request.headers['content-type'] == 'text/json'
```

# Dependencies

you will need **ONLY** if you decide to contribute to HTTPretty which
means you're gonna need run our test suite

* [nose](http://code.google.com/p/python-nose/)
* [sure](http://github.com/gabrielfalcao/sure/)
* [httplib2](http://code.google.com/p/httplib2/)
* [bolacha](http://github.com/gabrielfalcao/bolacha/)
* [tornado](http://tornadoweb.org/)
* [multiprocessing](http://code.google.com/p/python-multiprocessing/) **(only needed if you're running python < 2.6)**

## Here is a oneliner

### I know you want it :)

    pip install -r requirements.txt

# Contributing

1. fork and clone the project
2. install the dependencies above
3. run the tests with make:
    > make unit functional
4. hack at will
5. commit, push etc
6. send a pull request

# License

    <HTTPretty - HTTP client mock for Python>
    Copyright (C) <2011>  Gabriel Falcão <gabriel@nacaolivre.org>

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
