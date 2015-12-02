import httpretty
import requests


def test_get_all_requests():
    httpretty.register_uri(httpretty.POST, 'http://127.0.0.1:5001/notification')
    httpretty.enable()
    requests.post('http://127.0.0.1:5001/notification')
    requests.post('http://127.0.0.1:5001/notification?test=2')
    calls = httpretty.latest_requests()

    assert len(calls) == 2
    assert calls[0].querystring == {}
    assert calls[1].querystring == {u'test': [u'2']}

    httpretty.disable()
