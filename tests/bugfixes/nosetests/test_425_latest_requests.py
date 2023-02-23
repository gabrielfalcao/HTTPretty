import re
import requests
import httpretty
from httpretty.errors import UnmockedError

from unittest import skip
from sure import expect


@httpretty.activate(allow_net_connect=True)
def test_latest_requests():
    "#425 - httpretty.latest_requests() can be called multiple times"
    httpretty.register_uri(httpretty.GET, 'http://google.com/', body="Not Google")
    httpretty.register_uri(httpretty.GET, 'https://google.com/', body="Not Google")

    requests.get('http://google.com/')
    httpretty.latest_requests()[-1].url.should.equal('http://google.com/')
    requests.get('https://google.com/')
    httpretty.latest_requests()[-1].url.should.equal('https://google.com/')

    httpretty.latest_requests().should.have.length_of(2)
    httpretty.latest_requests()[-1].url.should.equal('https://google.com/')

    requests.get('https://google.com/')
    httpretty.latest_requests().should.have.length_of(3)
    httpretty.latest_requests()[-1].url.should.equal('https://google.com/')

    requests.get('http://google.com/')
    httpretty.latest_requests().should.have.length_of(4)
    httpretty.latest_requests()[-1].url.should.equal('http://google.com/')


@httpretty.activate(allow_net_connect=True)
def test_latest_requests_with_enable():
    "#425 - httpretty.latest_requests() can be called multiple times"
    httpretty.register_uri(httpretty.GET, 'https://google.com/', body="Not Google")

    requests.get('https://google.com/', data={"baz": "bar"})

    httpretty.latest_requests()[-1].url.should.equal('https://google.com/')
    httpretty.latest_requests().should.have.length_of(1)

