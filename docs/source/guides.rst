.. _guides:


Guides
######

A series of guides to using HTTPretty for various interesting
purposes.


.. _matching_urls_via_regular_expressions:

Matching URLs via regular expressions
=====================================

You can pass a compiled regular expression via :py:func:`re.compile`,
for example for intercepting all requests to a specific host.

**Example:**


.. literalinclude:: _static/regex-example.py
   :emphasize-lines: 8,10,13


Response Callbacks
==================



You can use the `body` parameter of
:py:meth:`~httpretty.core.httpretty.register_uri` in useful, practical
ways because it accepts a :py:func:`callable` as value.

As matter of example, this is analogous to `defining routes in Flask
<https://flask.palletsprojects.com/en/2.0.x/quickstart/#routing>`_ when combined with :ref:`matching urls via regular expressions <matching_urls_via_regular_expressions>`

This analogy breaks down, though, because HTTPretty does not provide
tools to make it easy to handle cookies, parse querystrings etc.

So far this has been a deliberate decision to keep HTTPretty operating
mostly at the TCP socket level.

Nothing prevents you from being creative with callbacks though, and as
you will see in the examples below, the request parameter is an
instance of :py:class:`~httpretty.core.HTTPrettyRequest` which has
everything you need to create elaborate fake APIs.


Defining callbacks
------------------

The body parameter callback must:

- Accept 3 arguments:

  - `request` - :py:class:`~httpretty.core.HTTPrettyRequest`
  - `uri` - :py:class:`str`
  - `headers` - :py:class:`dict` with default response headers (including the ones from the parameters ``adding_headers`` and ``forcing_headers`` of :py:meth:`~httpretty.core.httpretty.register_uri`

- Return 3 a tuple (or list) with 3 values

  - :py:class:`int` - HTTP Status Code
  - :py:class:`dict` - Response Headers
  - :py:class:`st` - Response Body

.. important::
   The **Content-Length** should match the byte length of the body.

   Changing **Content-Length** it in your handler can cause your HTTP
   client to misbehave, be very intentional when modifying it in our
   callback.

   The suggested way to manipulate headers is by modifying the
   response headers passed as argument and returning them in the tuple
   at the end.

   .. code:: python

      from typing import Tuple
      from httpretty.core import HTTPrettyRequest

      def my_callback(
              request: HTTPrettyRequest,
              url: str,
              headers: dict

          ) -> Tuple[int, dict, str]:

          headers['Content-Type'] = 'text/plain'
          return (200, headers, "the body")

    HTTPretty.register_uri(HTTPretty.GET, "https://test.com", body=my_callback)


Debug requests interactively with ipdb
--------------------------------------

The library `ipdb <https://pypi.org/project/ipdb/>`_ comes in handy to
introspect the request interactively with auto-complete via IPython.

.. literalinclude:: _static/guide-callback-regex-ipdb.py
   :emphasize-lines: 12,16,17

.. asciinema:: 415981
   :preload: 1


Emulating timeouts
------------------

In the bug report `#430
<https://github.com/gabrielfalcao/HTTPretty/issues/430>`_ the contributor `@mariojonke
<https://github.com/mariojonke>`_ provided a neat example of how to
emulate read timeout errors by "waiting" inside of a body callback.


.. literalinclude:: _static/read-timeout.py
   :emphasize-lines: 11-13,21,28
