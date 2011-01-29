# HTTPretty
> Version 0.1

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

This is a nice thing, if you consider that mostly python http module
will be "mockable".

# Usage

    from httpretty import HTTPretty
    HTTPretty.register_uri(HTTPretty.GET, "http://globo.com/",
                           body="The biggest portal in Brazil")

    fd = urllib2.urlopen('http://globo.com')
    got = fd.read()
    fd.close()

    print got

**:: output ::**

    The biggest portal in Brazil


# Dependencies

you will need **ONLY** if you decide to contribute to HTTPretty which means you're gonna need run our test suite

* [nose](http://code.google.com/p/python-nose/)
    > [sudo] pip install nose
* [sure](http://github.com/gabrielfalcao/sure/)
    > [sudo] pip install sure

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
