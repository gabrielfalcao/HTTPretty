import httpretty
import requests


@httpretty.activate
def test_test_ssl_bad_handshake():
    # Reproduces https://github.com/gabrielfalcao/HTTPretty/issues/242

    url_http = 'http://httpbin.org/status/200'
    url_https = 'https://github.com/gabrielfalcao/HTTPretty'

    httpretty.register_uri(httpretty.GET, url_http, body='insecure')
    httpretty.register_uri(httpretty.GET, url_https, body='encrypted')

    requests.get(url_http).text.should.equal('insecure')
    requests.get(url_https).text.should.equal('encrypted')
