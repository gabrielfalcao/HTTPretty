.. _introduction:

`Github <https://github.com/gabrielfalcao/HTTPretty>`_


What is HTTPretty ?
###################

.. highlight:: python

Once upon a time a python developer wanted to use a RESTful api,
everything was fine but until the day he needed to test the code that
hits the RESTful API: what if the API server is down? What if its
content has changed ?

Don't worry, HTTPretty is here for you:

::

  import requests
  import httpretty

  from sure import expect


  @httpretty.activate
  def test_yipit_api_returning_deals():
      httpretty.register_uri(httpretty.GET, "http://api.yipit.com/v1/deals/",
                             body='[{"title": "Test Deal"}]',
                             content_type="application/json")

      response = requests.get('http://api.yipit.com/v1/deals/')

      expect(response.json()).to.equal([{"title": "Test Deal"}])


A more technical description
============================

HTTPretty is a HTTP client mock library for Python 100% inspired on ruby's [FakeWeb](http://fakeweb.rubyforge.org/).
If you come from ruby this would probably sound familiar :smiley:

Installing
==========

Installing httpretty is as easy as:

.. highlight:: bash

::

   pip install httpretty


Demo
####

expecting a simple response body
================================


.. code:: python

   import requests
   import httpretty

   def test_one():
       httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
       httpretty.register_uri(httpretty.GET, "http://yipit.com/",
                              body="Find the best daily deals")

       response = requests.get('http://yipit.com')

       assert response.text == "Find the best daily deals"

       httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
       httpretty.reset()    # reset HTTPretty state (clean up registered urls and request history)


making assertions in a callback that generates the response body
================================================================

.. code:: python

   import requests
   import json
   import httpretty

   @httpretty.activate
   def test_with_callback_response():
     def request_callback(request, uri, response_headers):
         content_type = request.headers.get('Content-Type')
         assert request.body == '{"nothing": "here"}', 'unexpected body: {}'.format(request.body)
         assert content_type == 'application/json', 'expected application/json but received Content-Type: {}'.format(content_type)
         return [200, response_headers, json.dumps({"hello": "world"})]

     httpretty.register_uri(
         httpretty.POST, "https://httpretty.example.com/api",
         body=request_callback)

     response = requests.post('https://httpretty.example.com/api', headers={'Content-Type': 'application/json'}, data='{"nothing": "here"}')

     expect(response.json()).to.equal({"hello": "world"})


Link headers
============


 Tests link headers by using the `adding_headers` parameter.


 .. code:: python

    import requests
    from sure import expect
    import httpretty


    @httpretty.activate
    def test_link_response():
        first_url = "http://foo-api.com/data"
        second_url = "http://foo-api.com/data?page=2"
        link_str = "<%s>; rel='next'" % second_url

        httpretty.register_uri(
            httpretty.GET,
            first_url,
            body='{"success": true}',
            status=200,
            content_type="text/json",
            adding_headers={"Link": link_str},
        )
        httpretty.register_uri(
            httpretty.GET,
            second_url,
            body='{"success": false}',
            status=500,
            content_type="text/json",
        )
        # Performs a request to `first_url` followed by some testing
        response = requests.get(first_url)
        expect(response.json()).to.equal({"success": True})
        expect(response.status_code).to.equal(200)
        next_url = response.links["next"]["url"]
        expect(next_url).to.equal(second_url)

        # Follow the next URL and perform some testing.
        response2 = requests.get(next_url)
        expect(response2.json()).to.equal({"success": False})
        expect(response2.status_code).to.equal(500)


Motivation
##########

When building systems that access external resources such as RESTful
webservices, XMLRPC or even simple HTTP requests, we stumble in the
problem:

    *"I'm gonna need to mock all those requests"*

It brings a lot of hassle, you will need to use a generic mocking
tool, mess with scope and so on.

The idea behind HTTPretty (how it works)
========================================


HTTPretty `monkey patches <http://en.wikipedia.org/wiki/Monkey_patch>`_
Python's `socket <http://docs.python.org/library/socket.html>`_ core
module, reimplementing the HTTP protocol, by mocking requests and
responses.

As for how it works this way, you don't need to worry what http
library you're gonna use.

HTTPretty will mock the response for you :) *(and also give you the
latest requests so that you can check them)*
