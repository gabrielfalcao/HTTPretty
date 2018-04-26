Release Notes
=============

0.9.4
-----

Improvements:

- Official Python 3.6 support
- Normalized coding style to comform with PEP8 (partially)
- Add more API reference coverage in docstrings of members such as :py:class:`httpretty.core.Entry`
- Continuous Integration building python 2.7 and 3.6
- Migrate from `pip <https://pypi.org/project/pip/>`_ to `pipenv <https://docs.pipenv.org/>`_


0.8.4
-----

Improvements:

-  Refactored ``core.py`` and increased its unit test coverage to 80%.
   HTTPretty is slightly more robust now.

Bug fixes:

-  POST requests being called twice
   `#100 <https://github.com/gabrielfalcao/HTTPretty/pull/100>`__

0.6.5
-----

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

0.6.2
-----

-  Fixing bug of lack of trailing slashes
   `#73 <https://github.com/gabrielfalcao/HTTPretty/issues/73>`__
-  Applied pull requests
   `#71 <https://github.com/gabrielfalcao/HTTPretty/pull/71>`__ and
   `#72 <https://github.com/gabrielfalcao/HTTPretty/pull/72>`__ by
   @andresriancho
-  Keyword arg coercion fix by @dupuy
-  @papaeye fixed content-length calculation.

0.6.1
-----

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

0.5.14
------

-  Delegate calls to other methods on socket

-  `Normalized
   header <https://github.com/gabrielfalcao/HTTPretty/pull/49>`__
   strings

-  Callbacks are `more intelligent
   now <https://github.com/gabrielfalcao/HTTPretty/pull/47>`__

-  Normalize urls matching for url quoting

0.5.12
------

-  HTTPretty doesn't hang when using other application protocols under a
   @httprettified decorated test.

0.5.11
------

-  Ability to know whether HTTPretty is or not enabled through
   ``httpretty.is_enabled()``

0.5.10
------

-  Support to multiple methods per registered URL. Thanks @hughsaunders

0.5.9
-----

-  Fixed python 3 support. Thanks @spulec

0.5.8
-----

-  Support to `register regular expressions to match
   urls <#matching-regular-expressions>`__
-  `Body callback <#dynamic-responses-through-callbacks>`__ suppport
-  Python 3 support
