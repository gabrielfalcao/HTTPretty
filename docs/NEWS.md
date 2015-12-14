# Release Notes

## 0.8.11 (current)

Improvements:

* Refactored `core.py` and increased its unit test coverage to 80%. HTTPretty is slightly more robust now.

Bug fixes:

* POST requests being called twice [#100](https://github.com/gabrielfalcao/HTTPretty/pull/100)

## 0.6.5

Applied pull requests:

* continue on EAGAIN socket errors: [#102](https://github.com/gabrielfalcao/HTTPretty/pull/102) by [kouk](http://github.com/kouk).
* Fix `fake_gethostbyname` for requests 2.0: [#101](https://github.com/gabrielfalcao/HTTPretty/pull/101) by [mgood](http://github.com/mgood)
* Add a way to match the querystrings: [#98](https://github.com/gabrielfalcao/HTTPretty/pull/98) by [ametaireau](http://github.com/ametaireau)
* Use common string case for URIInfo hostname comparison: [#95](https://github.com/gabrielfalcao/HTTPretty/pull/95) by [mikewaters](http://github.com/mikewaters)
* Expose httpretty.reset() to public API: [#91](https://github.com/gabrielfalcao/HTTPretty/pull/91) by [imankulov](http://github.com/imankulov)
* Don't duplicate http ports number: [#89](https://github.com/gabrielfalcao/HTTPretty/pull/89) by [mardiros](http://github.com/mardiros)
* Adding parsed_body parameter to simplify checks: [#88](https://github.com/gabrielfalcao/HTTPretty/pull/88) by [toumorokoshi](http://github.com/toumorokoshi)
* Use the real socket if it's not HTTP: [#87](https://github.com/gabrielfalcao/HTTPretty/pull/87) by [mardiros](http://github.com/mardiros)

## 0.6.2

* Fixing bug of lack of trailing slashes [#73](https://github.com/gabrielfalcao/HTTPretty/issues/73)
* Applied pull requests [#71](https://github.com/gabrielfalcao/HTTPretty/pull/71) and [#72](https://github.com/gabrielfalcao/HTTPretty/pull/72) by @andresriancho
* Keyword arg coercion fix by @dupuy
* @papaeye fixed content-length calculation.

## 0.6.1

* New API, no more camel case and everything is available through a simple import:

```python
import httpretty

@httpretty.activate
def test_function():
    # httpretty.register_uri(...)
    # make request...
    pass
```

* Re-organized module into submodules

## 0.5.14

* Delegate calls to other methods on socket

* [Normalized header](https://github.com/gabrielfalcao/HTTPretty/pull/49) strings

* Callbacks are [more intelligent now](https://github.com/gabrielfalcao/HTTPretty/pull/47)

* Normalize urls matching for url quoting

## 0.5.12

* HTTPretty doesn't hang when using other application protocols under
  a @httprettified decorated test.

## 0.5.11

* Ability to know whether HTTPretty is or not enabled through `httpretty.is_enabled()`

## 0.5.10

* Support to multiple methods per registered URL. Thanks @hughsaunders

## 0.5.9

* Fixed python 3 support. Thanks @spulec

## 0.5.8

* Support to [register regular expressions to match urls](#matching-regular-expressions)
* [Body callback](#dynamic-responses-through-callbacks) suppport
* Python 3 support
