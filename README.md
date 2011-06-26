# HTTPretty
> Version 0.2

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

This is a nice thing, if you consider that all python http modules
are supposed to get mocked.

# Usage

## expecting a simple response body

```python
from httpretty import HTTPretty
HTTPretty.register_uri(HTTPretty.GET, "http://globo.com/",
                       body="The biggest portal in Brazil")

fd = urllib2.urlopen('http://globo.com')
got = fd.read()
fd.close()

print got
```

**:: output ::**

    The biggest portal in Brazil

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

# Documentation

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
