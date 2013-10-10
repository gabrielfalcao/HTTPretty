# Acknowledgements

## caveats with the [requests](http://docs.python-requests.org/en/latest/) library

### `forcing_headers` + `Content-Length`

if you use the `forcing_headers` options make sure to add the header
`Content-Length` otherwise the
[requests](http://docs.python-requests.org/en/latest/) will try to
load the response endlessly

# Officially supported libraries

Because HTTPretty works in the socket level it should work with any HTTP client libraries, although it is [battle tested](https://github.com/gabrielfalcao/HTTPretty/tree/master/tests/functional) against:

* [requests](http://docs.python-requests.org/en/latest/)
* [httplib2](http://code.google.com/p/httplib2/)
* [urllib2](http://docs.python.org/2/library/urllib2.html)
