import httpretty
import requests


@httpretty.activate
def test_something():
    import eventlet
    httpretty.register_uri(httpretty.GET, 'https://example.com', body='foo')
    requests.get('https://example.com').text.should.equal('foo')
