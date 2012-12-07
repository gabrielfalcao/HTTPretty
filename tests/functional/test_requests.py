# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import requests
from sure import within, microseconds, expect
from httpretty import HTTPretty, httprettified


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_a_simple_get_with_requests_read(now):
    u"HTTPretty should mock a simple GET with requests.get"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    response = requests.get('http://yipit.com')
    expect(response.text).to.equal('Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/')


@httprettified
@within(two=microseconds)
def test_httpretty_should_mock_headers_requests(now):
    u"HTTPretty should mock basic headers with requests"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/",
                           body="this is supposed to be the response",
                           status=201)

    response = requests.get('http://github.com')
    expect(response.status_code).to.equal(201)

    expect(dict(response.headers)).to.equal({
        'content-type': 'text/plain; charset=utf-8',
        'connection': 'close',
        'content-length': '35',
        'status': '201',
        'server': 'Python/HTTPretty',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_requests(now):
    u"HTTPretty should allow adding and overwritting headers with requests"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="this is supposed to be the response",
                           adding_headers={
                               'Server': 'Apache',
                               'Content-Length': '27',
                               'Content-Type': 'application/json',
                           })

    response = requests.get('http://github.com/foo')

    expect(dict(response.headers)).to.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_forcing_headers_requests(now):
    u"HTTPretty should allow forcing headers with requests"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="<root><baz /</root>",
                           forcing_headers={
                               'Content-Type': 'application/xml',
                               'Content-Length': '19',
                           })

    response = requests.get('http://github.com/foo')

    expect(dict(response.headers)).to.equal({
        'content-type': 'application/xml',
        'content-length': '19',
    })


@httprettified
@within(two=microseconds)
def test_httpretty_should_allow_adding_and_overwritting_by_kwargs_u2(now):
    u"HTTPretty should allow adding and overwritting headers by keyword args " \
        "with requests"

    HTTPretty.register_uri(HTTPretty.GET, "http://github.com/foo",
                           body="this is supposed to be the response",
                           server='Apache',
                           content_length='27',
                           content_type='application/json')

    response = requests.get('http://github.com/foo')

    expect(dict(response.headers)).to.equal({
        'content-type': 'application/json',
        'connection': 'close',
        'content-length': '27',
        'status': '200',
        'server': 'Apache',
        'date': now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })


@httprettified
@within(two=microseconds)
def test_rotating_responses_with_requests(now):
    u"HTTPretty should support rotating responses with requests"

    HTTPretty.register_uri(
        HTTPretty.GET, "https://api.yahoo.com/test",
        responses=[
            HTTPretty.Response(body="first response", status=201),
            HTTPretty.Response(body='second and last response', status=202),
        ])

    response1 = requests.get(
        'https://api.yahoo.com/test')

    expect(response1.status_code).to.equal(201)
    expect(response1.text).to.equal('first response')

    response2 = requests.get(
        'https://api.yahoo.com/test')

    expect(response2.status_code).to.equal(202)
    expect(response2.text).to.equal('second and last response')

    response3 = requests.get(
        'https://api.yahoo.com/test')

    expect(response3.status_code).to.equal(202)
    expect(response3.text).to.equal('second and last response')


@httprettified
@within(two=microseconds)
def test_can_inspect_last_request(now):
    u"HTTPretty.last_request is a mimetools.Message request from last match"

    HTTPretty.register_uri(HTTPretty.POST, "http://api.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    response = requests.post(
        'http://api.github.com',
        '{"username": "gabrielfalcao"}',
        headers={
            'content-type': 'text/json',
        },
    )

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        '{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(response.json).to.equal({"repositories": ["HTTPretty", "lettuce"]})


@httprettified
@within(two=microseconds)
def test_can_inspect_last_request_with_ssl(now):
    u"HTTPretty.last_request is recorded even when mocking 'https' (SSL)"

    HTTPretty.register_uri(HTTPretty.POST, "https://secure.github.com/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    response = requests.post(
        'https://secure.github.com',
        '{"username": "gabrielfalcao"}',
        headers={
            'content-type': 'text/json',
        },
    )

    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.body).to.equal(
        '{"username": "gabrielfalcao"}',
    )
    expect(HTTPretty.last_request.headers['content-type']).to.equal(
        'text/json',
    )
    expect(response.json).to.equal({"repositories": ["HTTPretty", "lettuce"]})


@httprettified
@within(two=microseconds)
def test_httpretty_ignores_querystrings_from_registered_uri(now):
    u"HTTPretty should ignore querystrings from the registered uri (requests library)"

    HTTPretty.register_uri(HTTPretty.GET, "http://yipit.com/?id=123",
                           body="Find the best daily deals")

    response = requests.get('http://yipit.com/', params={'id': 123})
    expect(response.text).to.equal('Find the best daily deals')
    expect(HTTPretty.last_request.method).to.equal('GET')
    expect(HTTPretty.last_request.path).to.equal('/?id=123')

@httprettified
@within(five=microseconds)
def test_streaming_responses(now):
    """
    Mock a streaming HTTP response, like those returned by the Twitter streaming
    API.
    """
    from contextlib import contextmanager
    @contextmanager
    def in_time(time, message):
        """
        A context manager that uses signals to force a time limit in tests
        (unlike the `@within` decorator, which only complains afterward), or
        raise an AssertionError.
        """
        import signal
        def handler(signum, frame):
            raise AssertionError(message)
        signal.signal(signal.SIGALRM, handler)
        signal.setitimer(signal.ITIMER_REAL, time)
        yield
        signal.setitimer(signal.ITIMER_REAL, 0)


    #XXX this obviously isn't a fully functional twitter streaming client!
    twitter_response_lines = [
        '{"text":"If \\"for the boobs\\" requests to follow me one more time I\'m calling the police. http://t.co/a0mDEAD8"}\r\n',
        '\r\n',
        '{"text":"RT @onedirection: Thanks for all your #FollowMe1D requests Directioners! We\u2019ll be following 10 people throughout the day starting NOW. G ..."}\r\n'
    ]

    TWITTER_STREAMING_URL = "https://stream.twitter.com/1/statuses/filter.json"

    HTTPretty.register_uri(HTTPretty.POST, TWITTER_STREAMING_URL,
                           body=(l for l in twitter_response_lines),
                           streaming=True)

    # taken from the requests docs
    # http://docs.python-requests.org/en/latest/user/advanced/#streaming-requests
    response = requests.post(TWITTER_STREAMING_URL, data={'track':'requests'},
                            auth=('username','password'), prefetch=False)

    #test iterating by line
    line_iter = response.iter_lines()
    with in_time(0.01, 'Iterating by line is taking forever!'):
        for i in xrange(len(twitter_response_lines)):
            expect(line_iter.next().strip()).to.equal(
                twitter_response_lines[i].strip())

    #test iterating by line after a second request
    response = requests.post(TWITTER_STREAMING_URL, data={'track':'requests'},
                            auth=('username','password'), prefetch=False)

    line_iter = response.iter_lines()
    with in_time(0.01, 'Iterating by line is taking forever the second time '
                       'around!'):
        for i in xrange(len(twitter_response_lines)):
            expect(line_iter.next().strip()).to.equal(
                twitter_response_lines[i].strip())

    #test iterating by char
    response = requests.post(TWITTER_STREAMING_URL, data={'track':'requests'},
                            auth=('username','password'), prefetch=False)

    twitter_expected_response_body = ''.join(twitter_response_lines)
    with in_time(0.02, 'Iterating by char is taking forever!'):
        twitter_body = u''.join(c for c in response.iter_content(chunk_size=1))

    expect(twitter_body).to.equal(twitter_expected_response_body)

    #test iterating by chunks larger than the stream

    response = requests.post(TWITTER_STREAMING_URL, data={'track':'requests'},
                            auth=('username','password'), prefetch=False)

    with in_time(0.02, 'Iterating by large chunks is taking forever!'):
        twitter_body = u''.join(c for c in
                                response.iter_content(chunk_size=1024))

    expect(twitter_body).to.equal(twitter_expected_response_body)

@httprettified
def test_multiline():
    url = 'http://httpbin.org/post'
    data = 'content=Im\r\na multiline\r\n\r\nsentence\r\n'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Accept': 'text/plain',
    }
    HTTPretty.register_uri(
        HTTPretty.POST,
        url,
    )
    response = requests.post(url, data=data, headers=headers )
    expect(response.status_code).to.equal(200)
    expect(HTTPretty.last_request.method).to.equal('POST')
    expect(HTTPretty.last_request.path).to.equal('/post')
    expect(HTTPretty.last_request.body).to.equal('content=Im\r\na multiline\r\n\r\nsentence\r\n')