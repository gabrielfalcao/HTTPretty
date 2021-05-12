Acknowledgements
################

Caveats
=======

``forcing_headers`` + ``Content-Length``
----------------------------------------

When using the ``forcing_headers`` option make sure to add the header
``Content-Length`` otherwise calls using :py:mod:`requests` will try
to load the response endlessly.

Supported Libraries
-------------------

Because HTTPretty works in the socket level it should work with any HTTP client libraries, although it is `battle tested <https://github.com/gabrielfalcao/HTTPretty/tree/master/tests/functional>`_ against:

* `requests <http://docs.python-requests.org/en/latest/>`_
* `httplib2 <http://code.google.com/p/httplib2/>`_
* `urllib2 <http://docs.python.org/2/library/urllib2.html>`_
