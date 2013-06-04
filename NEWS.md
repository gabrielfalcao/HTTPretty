### New in version 0.6.1

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

### New in version 0.5.14

* Delegate calls to other methods on socket

* [Normalized header](https://github.com/gabrielfalcao/HTTPretty/pull/49) strings

* Callbacks are [more intelligent now](https://github.com/gabrielfalcao/HTTPretty/pull/47)

* Normalize urls matching for url quoting

### New in version 0.5.12

* HTTPretty doesn't hang when using other application protocols under
  a @httprettified decorated test.

### New in version 0.5.11

* Ability to know whether HTTPretty is or not enabled through `httpretty.is_enabled()`

### New in version 0.5.10

* Support to multiple methods per registered URL. Thanks @hughsaunders

### New in version 0.5.9

* Fixed python 3 support. Thanks @spulec

### New in version 0.5.8

* Support to [register regular expressions to match urls](#matching-regular-expressions)
* [Body callback](#dynamic-responses-through-callbacks) suppport
* Python 3 support
