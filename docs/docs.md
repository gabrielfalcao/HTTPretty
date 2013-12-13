# Reference

## testing query strings

```python
import requests
from sure import expect
import httpretty

def test_one():
    httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
    httpretty.register_uri(httpretty.GET, "http://yipit.com/login",
                           body="Find the best daily deals")

    requests.get('http://yipit.com/login?email=user@github.com&password=foobar123')
    expect(httpretty.last_request()).to.have.property("querystring").being.equal({
        "email": "user@github.com",
        "password": "foobar123",
    })

    httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
```


## Using the decorator

**YES** we've got a decorator

```python
import requests
import httpretty

@httpretty.activate
def test_one():
    httpretty.register_uri(httpretty.GET, "http://yipit.com/",
                           body="Find the best daily deals")

    response = requests.get('http://yipit.com')
    assert response.text == "Find the best daily deals"
```

the `@httpretty.activate` is a short-hand decorator that wraps the
decorated function with httpretty.enable() and then calls
httpretty.disable() right after.

## Providing status code

```python
import requests
from sure import expect
import httpretty

@httpretty.activate
def test_github_access():
    httpretty.register_uri(httpretty.GET, "http://github.com/",
                           body="here is the mocked body",
                           status=201)

    response = requests.get('http://github.com')
    expect(response.status_code).to.equal(201)
```

## Providing custom heades

**and all you need is to add keyword args in which the keys are always lower-cased and with underscores `_` instead of dashes `-`**

For example, let's say you want to mock that server returns `content-type`.
To do so, use the argument `content_type`, **all the keyword args are taken by HTTPretty and transformed in the RFC2616 equivalent name**.

```python
@httpretty.activate
def test_some_api():
    httpretty.register_uri(httpretty.GET, "http://foo-api.com/gabrielfalcao",
                           body='{"success": false}',
                           status=500,
                           content_type='text/json')

    response = requests.get('http://foo-api.com/gabrielfalcao')

    expect(response.json()).to.equal({'success': False})
    expect(response.status_code).to.equal(500)
```


### Adding extra headers and forcing headers

You can pass the `adding_headers` argument as a dictionary and your
headers will be
[united](http://en.wikipedia.org/wiki/Union_(set_theory)) to the
existing headers.

```python
@httpretty.activate
def test_some_api():
    httpretty.register_uri(httpretty.GET, "http://foo-api.com/gabrielfalcao",
                           body='{"success": false}',
                           status=500,
                           content_type='text/json',
                           adding_headers={
                               'X-foo': 'bar'
                           })

    response = requests.get('http://foo-api.com/gabrielfalcao')

    expect(response.json()).to.equal({'success': False})
    expect(response.status_code).to.equal(500)
```

Although there are some situation where some headers line
`content-length` will be calculated by HTTPretty based on the
specified fake response body.

So you might want to *"force"* those headers:

```python
@httpretty.activate
def test_some_api():
    httpretty.register_uri(httpretty.GET, "http://foo-api.com/gabrielfalcao",
                           body='{"success": false}',
                           status=500,
                           content_type='text/json',
                           forcing_headers={
                               'content-length': '100'
                           })

    response = requests.get('http://foo-api.com/gabrielfalcao')

    expect(response.json()).to.equal({'success': False})
    expect(response.status_code).to.equal(500)
```

You should, though, be careful with it. The HTTP client is likely to
rely on the content length to know how many bytes of response payload
should be loaded. Forcing a `content-length` that is bigger than the
action response body might cause the HTTP client to hang because it is
waiting for data. Read more in the "caveats" session on the bottom.

## rotating responses

Same URL, same request method, the first request return the first
httpretty.Response, all the subsequent ones return the last (status 202).

Notice that the `responses` argument is a list and you can pass as
many responses as you want.

```python
import requests
from sure import expect


@httpretty.activate
def test_rotating_responses():
    httpretty.register_uri(httpretty.GET, "http://github.com/gabrielfalcao/httpretty",
                           responses=[
                               httpretty.Response(body="first response", status=201),
                               httpretty.Response(body='second and last response', status=202),
                            ])

    response1 = requests.get('http://github.com/gabrielfalcao/httpretty')
    expect(response1.status_code).to.equal(201)
    expect(response1.text).to.equal('first response')

    response2 = requests.get('http://github.com/gabrielfalcao/httpretty')
    expect(response2.status_code).to.equal(202)
    expect(response2.text).to.equal('second and last response')

    response3 = requests.get('http://github.com/gabrielfalcao/httpretty')

    expect(response3.status_code).to.equal(202)
    expect(response3.text).to.equal('second and last response')
```
## streaming responses

Mock a streaming response by registering a generator response body.

```python
import requests
from sure import expect
import httpretty

# mock a streaming response body with a generator
def mock_streaming_tweets(tweets):
    from time import sleep
    for t in tweets:
        sleep(.5)
        yield t

@httpretty.activate
def test_twitter_api_integration(now):
    twitter_response_lines = [
        '{"text":"If @BarackObama requests to follow me one more time I\'m calling the police."}\r\n',
        '\r\n',
        '{"text":"Thanks for all your #FollowMe1D requests Directioners! We\u2019ll be following 10 people throughout the day starting NOW. G ..."}\r\n'
    ]

    TWITTER_STREAMING_URL = "https://stream.twitter.com/1/statuses/filter.json"

    # set the body to a generator and set `streaming=True` to mock a streaming response body
    httpretty.register_uri(httpretty.POST, TWITTER_STREAMING_URL,
                           body=mock_streaming_tweets(twitter_response_lines),
                           streaming=True)

    # taken from the requests docs
    # http://docs.python-requests.org/en/latest/user/advanced/#streaming-requests
    response = requests.post(TWITTER_STREAMING_URL, data={'track':'requests'},
                            auth=('username','password'), prefetch=False)

    #test iterating by line
    line_iter = response.iter_lines()
    for i in xrange(len(twitter_response_lines)):
        expect(line_iter.next().strip()).to.equal(twitter_response_lines[i].strip())
```

## dynamic responses through callbacks

Set a callback to allow for dynamic responses based on the request.

```python
import requests
from sure import expect
import httpretty

@httpretty.activate
def test_response_callbacks():

    def request_callback(request, uri, headers):
        return (200, headers, "The {} response from {}".format(request.method, uri))

    httpretty.register_uri(
        httpretty.GET, "https://api.yahoo.com/test",
        body=request_callback)

    response = requests.get('https://api.yahoo.com/test')

    expect(response.text).to.equal('The GET response from https://api.yahoo.com/test')
```

## matching regular expressions

You can register a
[compiled regex](http://docs.python.org/2/library/re.html#re.compile)
and it will be matched against the requested urls.

```python
@httpretty.activate
def test_httpretty_should_allow_registering_regexes():
    u"HTTPretty should allow registering regexes"

    httpretty.register_uri(
        httpretty.GET,
        re.compile("api.yipit.com/v2/deal;brand=(\w+)"),
        body="Found brand",
    )

    response = requests.get('https://api.yipit.com/v2/deal;brand=GAP')
    expect(response.text).to.equal('Found brand')
    expect(httpretty.last_request().method).to.equal('GET')
    expect(httpretty.last_request().path).to.equal('/v1/deal;brand=GAP')
```

By default, the regexp you register will match the requests without looking at
the querystring. If you want the querystring to be considered, you can set
`match_querystring=True` when calling `register_uri`.

## expect for a response, and check the request got by the "server" to make sure it was fine.

```python
import requests
from sure import expect
import httpretty


@httpretty.activate
def test_yipit_api_integration():
    httpretty.register_uri(httpretty.POST, "http://api.yipit.com/foo/",
                           body='{"repositories": ["HTTPretty", "lettuce"]}')

    response = requests.post('http://api.yipit.com/foo',
                            '{"username": "gabrielfalcao"}',
                            headers={
                                'content-type': 'text/json',
                            })

    expect(response.text).to.equal('{"repositories": ["HTTPretty", "lettuce"]}')
    expect(httpretty.last_request().method).to.equal("POST")
    expect(httpretty.last_request().headers['content-type']).to.equal('text/json')
```

## checking if is enabled

```python

httpretty.enable()
httpretty.is_enabled().should.be.true

httpretty.disable()
httpretty.is_enabled().should.be.false

```
