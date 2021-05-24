import requests, time
from threading import Event

from httpretty import httprettified
from httpretty import HTTPretty


@httprettified(allow_net_connect=False)
def test_read_timeout():
    event = Event()
    wait_seconds = 10
    connect_timeout = 0.1
    read_timeout = 0.1

    def my_callback(request, url, headers):
        event.wait(wait_seconds)
        return 200, headers, "Received"

    HTTPretty.register_uri(
        HTTPretty.GET, "http://example.com",
        body=my_callback
    )

    requested_at = time.time()
    try:
        requests.get(
            "http://example.com",
            timeout=(connect_timeout, read_timeout))
    except requests.exceptions.ReadTimeout:
        pass

    event_set_at = time.time()
    event.set()

    now = time.time()

    assert now - event_set_at < 0.2
    total_duration = now - requested_at
    assert total_duration < 0.2
