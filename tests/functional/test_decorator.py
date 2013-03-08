# coding: utf-8
from unittest import TestCase
from sure import expect
from httpretty import httprettified, HTTPretty

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


@httprettified
def test_decor():
    HTTPretty.register_uri(
        HTTPretty.GET, "http://localhost/",
        body="glub glub")

    fd = urllib2.urlopen('http://localhost/')
    got1 = fd.read()
    fd.close()

    expect(got1).to.equal(b'glub glub')


@httprettified
class ClassDecorator(TestCase):

    def test_decorated(self):
        HTTPretty.register_uri(
            HTTPretty.GET, "http://localhost/",
            body="glub glub")

        fd = urllib2.urlopen('http://localhost/')
        got1 = fd.read()
        fd.close()

        expect(got1).to.equal(b'glub glub')

    def test_decorated2(self):
        HTTPretty.register_uri(
            HTTPretty.GET, "http://localhost/",
            body="buble buble")

        fd = urllib2.urlopen('http://localhost/')
        got1 = fd.read()
        fd.close()

        expect(got1).to.equal(b'buble buble')