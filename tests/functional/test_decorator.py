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
class DecoratedNonUnitTest(object):

    def test_fail(self):
        raise AssertionError('Tests in this class should not '
                             'be executed by the test runner.')

    def test_decorated(self):
        HTTPretty.register_uri(
            HTTPretty.GET, "http://localhost/",
            body="glub glub")

        fd = urllib2.urlopen('http://localhost/')
        got1 = fd.read()
        fd.close()

        expect(got1).to.equal(b'glub glub')


class NonUnitTestTest(TestCase):
    """
    Checks that the test methods in DecoratedNonUnitTest were decorated.
    """

    def test_decorated(self):
        DecoratedNonUnitTest().test_decorated()


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


@httprettified
class ClassDecoratorWithSetUp(TestCase):

    def setUp(self):
        HTTPretty.register_uri(
            HTTPretty.GET, "http://localhost/",
            responses=[
                HTTPretty.Response("glub glub"),
                HTTPretty.Response("buble buble"),
            ])

    def test_decorated(self):

        fd = urllib2.urlopen('http://localhost/')
        got1 = fd.read()
        fd.close()

        expect(got1).to.equal(b'glub glub')

        fd = urllib2.urlopen('http://localhost/')
        got2 = fd.read()
        fd.close()

        expect(got2).to.equal(b'buble buble')

    def test_decorated2(self):

        fd = urllib2.urlopen('http://localhost/')
        got1 = fd.read()
        fd.close()

        expect(got1).to.equal(b'glub glub')

        fd = urllib2.urlopen('http://localhost/')
        got2 = fd.read()
        fd.close()

        expect(got2).to.equal(b'buble buble')
