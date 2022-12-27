import json
import requests
import httpretty
from httpretty.errors import UnmockedError

from unittest import skip
from sure import expect


@httpretty.activate(allow_net_connect=True)
def test_multiple_instances_of_same_header():
    "#399 - Issuing multiple instances of same header"

    def callback(request, url, headers):
        headers["Content-Type"] = "application/json"
        headers["Date"] = "Mon, 31 May 2021 17:47:51 GMT"
        headers["Set-Cookie"] = "foo;bar"

        return 200, headers, json.dumps(dict(request.headers))

    httpretty.register_uri(httpretty.GET, "https://httpbin.org/cookies", body=callback)

    jar = requests.cookies.RequestsCookieJar()
    jar.set("first_cookie", "first", domain="httpbin.org", path="/cookies")
    jar.set("second_cookie", "second", domain="httpbin.org", path="/extra")
    jar.set("third_cookie", "third", domain="httpbin.org", path="/cookies")
    jar.set("fourth_cookie", "fourth", domain="httpbin.org", path="/")

    url = "https://httpbin.org/cookies"
    response = requests.get(url, cookies=jar)

    response.json().should.equal(
        {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Cookie": "first_cookie=first; third_cookie=third; fourth_cookie=fourth",
            "Host": "httpbin.org",
            "User-Agent": "python-requests/2.25.1",
        }
    )
    dict(response.headers).should.equal(
        {
            "connection": "close",
            "content-length": "218",
            "set-cookie": "foo;bar",
            "content-type": "application/json",
            "server": "Python/HTTPretty",
            "date": "Mon, 31 May 2021 17:47:51 GMT",
            "status": "200",
        }
    )
