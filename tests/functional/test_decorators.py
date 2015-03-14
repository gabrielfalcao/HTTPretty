# coding: utf-8
from unittest import TestCase
from sure import expect
from httpretty import httprettified, HTTPretty
from httpretty.core import register

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


@httprettified
def test_httprettified_decorator():
    HTTPretty.register_uri(
        HTTPretty.GET, 'http://localhost/',
        body='glub glub')

    fd = urllib2.urlopen('http://localhost/')
    contents = fd.read()
    fd.close()
    expect(contents).to.equal(b'glub glub')


@httprettified
class HTTPrettifiedClass(TestCase):

    def setUp(self):
        self.assertFalse(HTTPretty.is_enabled())

    def tearDown(self):
        self.assertFalse(HTTPretty.is_enabled())

    def test_decorated(self):
        HTTPretty.register_uri(
            HTTPretty.GET, 'http://localhost/',
            body='glub glub')

        fd = urllib2.urlopen('http://localhost/')
        contents = fd.read()
        fd.close()

        expect(contents).to.equal(b'glub glub')

    def test_decorated2(self):
        HTTPretty.register_uri(
            HTTPretty.GET, 'http://localhost/',
            body='buble buble')

        fd = urllib2.urlopen('http://localhost/')
        contents = fd.read()
        fd.close()

        expect(contents).to.equal(b'buble buble')


@register(method=HTTPretty.GET, uri='http://localhost/', body='glub glub')
def test_register_uri_decorator():
    fd = urllib2.urlopen('http://localhost/')
    contents = fd.read()
    fd.close()
    expect(contents).to.equal(b'glub glub')


@register(method=HTTPretty.GET, uri='http://localhost/', body='bubble pop')
class HTTPregisterClass(TestCase):

    def setUp(self):
        self.assertFalse(HTTPretty.is_enabled())

    def tearDown(self):
        self.assertFalse(HTTPretty.is_enabled())

    def test_decorated(self):
        fd = urllib2.urlopen('http://localhost/')
        contents = fd.read()
        fd.close()

        expect(contents).to.equal(b'bubble pop')

    def test_decorated2(self):
        fd = urllib2.urlopen('http://localhost/')
        contents = fd.read()
        fd.close()

        expect(contents).to.equal(b'bubble pop')
