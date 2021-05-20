Release Notes
=============

Release 1.1.2
-------------

- Bugfix: `#426 <https://github.com/gabrielfalcao/HTTPretty/issues/426>`_ Segmentation fault when running against a large amount of tests with ``pytest --mypy``.

Release 1.1.1
-------------

- Bugfix: `httpretty.disable()` injects pyopenssl into :py:mod:`urllib3` even if it originally wasn't `#417 <https://github.com/gabrielfalcao/HTTPretty/issues/417>`_
- Bugfix: "Incompatibility with boto3 S3 put_object" `#416 <https://github.com/gabrielfalcao/HTTPretty/issues/416>`_
- Bugfix: "Regular expression for URL -> TypeError: wrap_socket() missing 1 required" `#413 <https://github.com/gabrielfalcao/HTTPretty/issues/413>`_
- Bugfix: "Making requests to non-stadard port throws TimeoutError "`#387 <https://github.com/gabrielfalcao/HTTPretty/issues/387>`_


Release 1.1.0
-------------

- Feature: Display mismatched URL within ``UnmockedError`` whenever possible. `#388 <https://github.com/gabrielfalcao/HTTPretty/issues/388>`_
- Feature: Display mismatched URL via logging. `#419 <https://github.com/gabrielfalcao/HTTPretty/pull/419>`_
- Add new properties to :py:class:`httpretty.core.HTTPrettyRequest` (``protocol, host, url, path, method``).

Example usage:

.. testcode::

   import httpretty
   import requests

   @httpretty.activate(verbose=True, allow_net_connect=False)
   def test_mismatches():
       requests.get('http://sql-server.local')
       requests.get('https://redis.local')


Release 1.0.5
-------------

- Bugfix: Support `socket.socketpair() <https://docs.python.org/3/library/socket.html#socket.socketpair>`_ . `#402 <https://github.com/gabrielfalcao/HTTPretty/issues/402>`_
- Bugfix: Prevent exceptions from re-applying monkey patches. `#406 <https://github.com/gabrielfalcao/HTTPretty/issues/406>`_

Release 1.0.4
-------------

- Python 3.8 and 3.9 support. `#407 <https://github.com/gabrielfalcao/HTTPretty/issues/407>`_

Release 1.0.3
-------------

- Fix compatibility with urllib3>=1.26. `#410 <https://github.com/gabrielfalcao/HTTPretty/pull/410>`_

Release 1.0.0
-------------

- Drop Python 2 support.
- Fix usage with redis and improve overall real-socket passthrough. `#271 <https://github.com/gabrielfalcao/HTTPretty/issues/271>`_.
- Fix TypeError: wrap_socket() missing 1 required positional argument: 'sock' (`#393 <https://github.com/gabrielfalcao/HTTPretty/pull/393>`_)
- Merge pull request `#364 <https://github.com/gabrielfalcao/HTTPretty/pull/364>`_
- Merge pull request `#371 <https://github.com/gabrielfalcao/HTTPretty/pull/371>`_
- Merge pull request `#379 <https://github.com/gabrielfalcao/HTTPretty/pull/379>`_
- Merge pull request `#386 <https://github.com/gabrielfalcao/HTTPretty/pull/386>`_
- Merge pull request `#302 <https://github.com/gabrielfalcao/HTTPretty/pull/302>`_
- Merge pull request `#373 <https://github.com/gabrielfalcao/HTTPretty/pull/373>`_
- Merge pull request `#383 <https://github.com/gabrielfalcao/HTTPretty/pull/383>`_
- Merge pull request `#385 <https://github.com/gabrielfalcao/HTTPretty/pull/385>`_
- Merge pull request `#389 <https://github.com/gabrielfalcao/HTTPretty/pull/389>`_
- Merge pull request `#391 <https://github.com/gabrielfalcao/HTTPretty/pull/391>`_
- Fix simple typo: neighter -> neither.
- Updated documentation for register_uri concerning using ports.
- Clarify relation between ``enabled`` and ``httprettized`` in API docs.
- Align signature with builtin socket.

Release 0.9.4
-------------

Improvements:

- Official Python 3.6 support
- Normalized coding style to comform with PEP8 (partially)
- Add more API reference coverage in docstrings of members such as :py:class:`httpretty.core.Entry`
- Continuous Integration building python 2.7 and 3.6
- Migrate from `pip <https://pypi.org/project/pip/>`_ to `pipenv <https://docs.pipenv.org/>`_


Release 0.8.4
-------------

Improvements:

-  Refactored ``core.py`` and increased its unit test coverage to 80%.
   HTTPretty is slightly more robust now.

Bug fixes:

-  POST requests being called twice
   `#100 <https://github.com/gabrielfalcao/HTTPretty/pull/100>`__

Release 0.6.5
-------------

Applied pull requests:

-  continue on EAGAIN socket errors:
   `#102 <https://github.com/gabrielfalcao/HTTPretty/pull/102>`__ by
   `kouk <http://github.com/kouk>`__.
-  Fix ``fake_gethostbyname`` for requests 2.0:
   `#101 <https://github.com/gabrielfalcao/HTTPretty/pull/101>`__ by
   `mgood <http://github.com/mgood>`__
-  Add a way to match the querystrings:
   `#98 <https://github.com/gabrielfalcao/HTTPretty/pull/98>`__ by
   `ametaireau <http://github.com/ametaireau>`__
-  Use common string case for URIInfo hostname comparison:
   `#95 <https://github.com/gabrielfalcao/HTTPretty/pull/95>`__ by
   `mikewaters <http://github.com/mikewaters>`__
-  Expose httpretty.reset() to public API:
   `#91 <https://github.com/gabrielfalcao/HTTPretty/pull/91>`__ by
   `imankulov <http://github.com/imankulov>`__
-  Don't duplicate http ports number:
   `#89 <https://github.com/gabrielfalcao/HTTPretty/pull/89>`__ by
   `mardiros <http://github.com/mardiros>`__
-  Adding parsed\_body parameter to simplify checks:
   `#88 <https://github.com/gabrielfalcao/HTTPretty/pull/88>`__ by
   `toumorokoshi <http://github.com/toumorokoshi>`__
-  Use the real socket if it's not HTTP:
   `#87 <https://github.com/gabrielfalcao/HTTPretty/pull/87>`__ by
   `mardiros <http://github.com/mardiros>`__

Release 0.6.2
-------------

-  Fixing bug of lack of trailing slashes
   `#73 <https://github.com/gabrielfalcao/HTTPretty/issues/73>`__
-  Applied pull requests
   `#71 <https://github.com/gabrielfalcao/HTTPretty/pull/71>`__ and
   `#72 <https://github.com/gabrielfalcao/HTTPretty/pull/72>`__ by
   @andresriancho
-  Keyword arg coercion fix by @dupuy
-  @papaeye fixed content-length calculation.

Release 0.6.1
-------------

-  New API, no more camel case and everything is available through a
   simple import:

.. code:: python

    import httpretty

    @httpretty.activate
    def test_function():
        # httpretty.register_uri(...)
        # make request...
        pass

-  Re-organized module into submodules

Release 0.5.14
--------------

-  Delegate calls to other methods on socket

-  `Normalized
   header <https://github.com/gabrielfalcao/HTTPretty/pull/49>`__
   strings

-  Callbacks are `more intelligent
   now <https://github.com/gabrielfalcao/HTTPretty/pull/47>`__

-  Normalize urls matching for url quoting

Release 0.5.12
--------------

-  HTTPretty doesn't hang when using other application protocols under a
   @httprettified decorated test.

Release 0.5.11
--------------

-  Ability to know whether HTTPretty is or not enabled through
   ``httpretty.is_enabled()``

Release 0.5.10
--------------

-  Support to multiple methods per registered URL. Thanks @hughsaunders

Release 0.5.9
-------------

-  Fixed python 3 support. Thanks @spulec

Release 0.5.8
-------------

-  Support to `register regular expressions to match
   urls <#matching-regular-expressions>`__
-  `Body callback <#dynamic-responses-through-callbacks>`__ suppport
-  Python 3 support
