import re
import requests
import httpretty


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_regex():
    httpretty.register_uri(httpretty.GET, re.compile(r'.*'), status=418)

    response1 = requests.get('http://foo.com')
    assert response1.status_code == 418

    response2 = requests.get('http://test.com')
    assert response2.status_code == 418
