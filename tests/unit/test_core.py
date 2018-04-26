# #!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import errno
from datetime import datetime

from mock import Mock, patch, call
from sure import expect

from httpretty.compat import StringIO
from httpretty.core import HTTPrettyRequest, FakeSSLSocket, fakesock, httpretty


class SocketErrorStub(Exception):
    def __init__(self, errno):
        self.errno = errno


def test_request_stubs_internals():
    ("HTTPrettyRequest is a BaseHTTPRequestHandler that replaces "
     "real socket file descriptors with in-memory ones")

    # Given a valid HTTP request header string
    headers = "\r\n".join([
        'POST /somewhere/?name=foo&age=bar HTTP/1.1',
        'accept-encoding: identity',
        'host: github.com',
        'content-type: application/json',
        'connection: close',
        'user-agent: Python-urllib/2.7',
    ])

    # When I create a HTTPrettyRequest with an empty body
    request = HTTPrettyRequest(headers, body='')

    # Then it should have parsed the headers
    dict(request.headers).should.equal({
        'accept-encoding': 'identity',
        'connection': 'close',
        'content-type': 'application/json',
        'host': 'github.com',
        'user-agent': 'Python-urllib/2.7'
    })

    # And the `rfile` should be a StringIO
    type_as_str = StringIO.__module__ + '.' + StringIO.__name__

    request.should.have.property('rfile').being.a(type_as_str)

    # And the `wfile` should be a StringIO
    request.should.have.property('wfile').being.a(type_as_str)

    # And the `method` should be available
    request.should.have.property('method').being.equal('POST')


def test_request_parse_querystring():
    ("HTTPrettyRequest#parse_querystring should parse unicode data")

    # Given a request string containing a unicode encoded querystring

    headers = "\r\n".join([
        'POST /create?name=Gabriel+Falcão HTTP/1.1',
        'Content-Type: multipart/form-data',
    ])

    # When I create a HTTPrettyRequest with an empty body
    request = HTTPrettyRequest(headers, body='')

    # Then it should have a parsed querystring
    request.querystring.should.equal({'name': ['Gabriel Falcão']})


def test_request_parse_body_when_it_is_application_json():
    ("HTTPrettyRequest#parse_request_body recognizes the "
     "content-type `application/json` and parses it")

    # Given a request string containing a unicode encoded querystring
    headers = "\r\n".join([
        'POST /create HTTP/1.1',
        'Content-Type: application/json',
    ])
    # And a valid json body
    body = json.dumps({'name': 'Gabriel Falcão'})

    # When I create a HTTPrettyRequest with that data
    request = HTTPrettyRequest(headers, body)

    # Then it should have a parsed body
    request.parsed_body.should.equal({'name': 'Gabriel Falcão'})


def test_request_parse_body_when_it_is_text_json():
    ("HTTPrettyRequest#parse_request_body recognizes the "
     "content-type `text/json` and parses it")

    # Given a request string containing a unicode encoded querystring
    headers = "\r\n".join([
        'POST /create HTTP/1.1',
        'Content-Type: text/json',
    ])
    # And a valid json body
    body = json.dumps({'name': 'Gabriel Falcão'})

    # When I create a HTTPrettyRequest with that data
    request = HTTPrettyRequest(headers, body)

    # Then it should have a parsed body
    request.parsed_body.should.equal({'name': 'Gabriel Falcão'})


def test_request_parse_body_when_it_is_urlencoded():
    ("HTTPrettyRequest#parse_request_body recognizes the "
     "content-type `application/x-www-form-urlencoded` and parses it")

    # Given a request string containing a unicode encoded querystring
    headers = "\r\n".join([
        'POST /create HTTP/1.1',
        'Content-Type: application/x-www-form-urlencoded',
    ])
    # And a valid urlencoded body
    body = "name=Gabriel+Falcão&age=25&projects=httpretty&projects=sure&projects=lettuce"

    # When I create a HTTPrettyRequest with that data
    request = HTTPrettyRequest(headers, body)

    # Then it should have a parsed body
    request.parsed_body.should.equal({
        'name': ['Gabriel Falcão'],
        'age': ["25"],
        'projects': ["httpretty", "sure", "lettuce"]
    })


def test_request_parse_body_when_unrecognized():
    ("HTTPrettyRequest#parse_request_body returns the value as "
     "is if the Content-Type is not recognized")

    # Given a request string containing a unicode encoded querystring
    headers = "\r\n".join([
        'POST /create HTTP/1.1',
        'Content-Type: whatever',
    ])
    # And a valid urlencoded body
    body = "foobar:\nlalala"

    # When I create a HTTPrettyRequest with that data
    request = HTTPrettyRequest(headers, body)

    # Then it should have a parsed body
    request.parsed_body.should.equal("foobar:\nlalala")


def test_request_string_representation():
    ("HTTPrettyRequest should have a debug-friendly "
     "string representation")

    # Given a request string containing a unicode encoded querystring
    headers = "\r\n".join([
        'POST /create HTTP/1.1',
        'Content-Type: JPEG-baby',
    ])
    # And a valid urlencoded body
    body = "foobar:\nlalala"

    # When I create a HTTPrettyRequest with that data
    request = HTTPrettyRequest(headers, body)

    # Then its string representation should show the headers and the body
    str(request).should.equal('<HTTPrettyRequest("JPEG-baby", total_headers=1, body_length=14)>')


def test_fake_ssl_socket_proxies_its_ow_socket():
    ("FakeSSLSocket is a simpel wrapper around its own socket, "
     "which was designed to be a HTTPretty fake socket")

    # Given a sentinel mock object
    socket = Mock()

    # And a FakeSSLSocket wrapping it
    ssl = FakeSSLSocket(socket)

    # When I make a method call
    ssl.send("FOO")

    # Then it should bypass any method calls to its own socket
    socket.send.assert_called_once_with("FOO")


@patch('httpretty.core.datetime')
def test_fakesock_socket_getpeercert(dt):
    ("fakesock.socket#getpeercert should return a hardcoded fake certificate")
    # Background:
    dt.now.return_value = datetime(2013, 10, 4, 4, 20, 0)

    # Given a fake socket instance
    socket = fakesock.socket()

    # And that it's bound to some host and port
    socket.connect(('somewhere.com', 80))

    # When I retrieve the peer certificate
    certificate = socket.getpeercert()

    # Then it should return a hardcoded value
    certificate.should.equal({
        u'notAfter': 'Sep 29 04:20:00 GMT',
        u'subject': (
            ((u'organizationName', u'*.somewhere.com'),),
            ((u'organizationalUnitName', u'Domain Control Validated'),),
            ((u'commonName', u'*.somewhere.com'),)),
        u'subjectAltName': (
            (u'DNS', u'*somewhere.com'),
            (u'DNS', u'somewhere.com'),
            (u'DNS', u'*')
        )
    })


def test_fakesock_socket_ssl():
    ("fakesock.socket#ssl should take a socket instance and return itself")
    # Given a fake socket instance
    socket = fakesock.socket()

    # And a stubbed socket sentinel
    sentinel = Mock()

    # When I call `ssl` on that mock
    result = socket.ssl(sentinel)

    # Then it should have returned its first argument
    result.should.equal(sentinel)


@patch('httpretty.core.old_socket')
@patch('httpretty.core.POTENTIAL_HTTP_PORTS')
def test_fakesock_socket_connect_fallback(POTENTIAL_HTTP_PORTS, old_socket):
    ("fakesock.socket#connect should open a real connection if the "
     "given port is not a potential http port")
    # Background: the potential http ports are 80 and 443
    POTENTIAL_HTTP_PORTS.__contains__.side_effect = lambda other: int(other) in (80, 443)

    # Given a fake socket instance
    socket = fakesock.socket()

    # When it is connected to a remote server in a port that isn't 80 nor 443
    socket.connect(('somewhere.com', 42))

    # Then it should have open a real connection in the background
    old_socket.return_value.connect.assert_called_once_with(('somewhere.com', 42))

    # And _closed is set to False
    socket._closed.should.be.false


@patch('httpretty.core.old_socket')
def test_fakesock_socket_close(old_socket):
    ("fakesock.socket#close should close the actual socket in case "
     "it's not http and _closed is False")
    # Given a fake socket instance that is synthetically open
    socket = fakesock.socket()
    socket._closed = False
    socket._connected_truesock = True

    # When I close it
    socket.close()

    # Then its real socket should have been closed
    old_socket.return_value.close.assert_called_once_with()

    # And _closed is set to True
    socket._closed.should.be.true


@patch('httpretty.core.old_socket')
def test_fakesock_socket_makefile(old_socket):
    ("fakesock.socket#makefile should set the mode, "
     "bufsize and return its mocked file descriptor")

    # Given a fake socket that has a mocked Entry associated with it
    socket = fakesock.socket()
    socket._entry = Mock()

    # When I call makefile()
    fd = socket.makefile(mode='rw', bufsize=512)

    # Then it should have returned the socket's own filedescriptor
    expect(fd).to.equal(socket.fd)
    # And the mode should have been set in the socket instance
    socket._mode.should.equal('rw')
    # And the bufsize should have been set in the socket instance
    socket._bufsize.should.equal(512)

    # And the entry should have been filled with that filedescriptor
    socket._entry.fill_filekind.assert_called_once_with(fd)


@patch('httpretty.core.old_socket')
def test_fakesock_socket_real_sendall(old_socket):
    ("fakesock.socket#real_sendall calls truesock#connect and bails "
     "out when not http")
    # Background: the real socket will stop returning bytes after the
    # first call
    real_socket = old_socket.return_value
    real_socket.recv.side_effect = [b'response from server', b""]

    # Given a fake socket
    socket = fakesock.socket()

    # When I call real_sendall with data, some args and kwargs
    socket.real_sendall(b"SOMEDATA", b'some extra args...', foo=b'bar')

    # Then it should have called sendall in the real socket
    real_socket.sendall.assert_called_once_with(b"SOMEDATA", b'some extra args...', foo=b'bar')

    # And setblocking was never called
    real_socket.setblocking.called.should.be.false

    # And recv was never called
    real_socket.recv.called.should.be.false

    # And the buffer is empty
    socket.fd.read().should.equal(b'')

    # And connect was never called
    real_socket.connect.called.should.be.false


@patch('httpretty.core.old_socket')
def test_fakesock_socket_real_sendall_when_http(old_socket):
    ("fakesock.socket#real_sendall sends data and buffers "
     "the response in the file descriptor")
    # Background: the real socket will stop returning bytes after the
    # first call
    real_socket = old_socket.return_value
    real_socket.recv.side_effect = [b'response from server', b""]

    # Given a fake socket
    socket = fakesock.socket()
    socket.is_http = True

    # When I call real_sendall with data, some args and kwargs
    socket.real_sendall(b"SOMEDATA", b'some extra args...', foo=b'bar')

    # Then it should have called sendall in the real socket
    real_socket.sendall.assert_called_once_with(b"SOMEDATA", b'some extra args...', foo=b'bar')

    # And the socket was set to blocking
    real_socket.setblocking.assert_called_once_with(1)

    # And recv was called with the bufsize
    real_socket.recv.assert_has_calls([
        call(socket._bufsize)
    ])

    # And the buffer should contain the data from the server
    socket.fd.read().should.equal(b"response from server")

    # And connect was called
    real_socket.connect.called.should.be.true


@patch('httpretty.core.old_socket')
@patch('httpretty.core.socket')
def test_fakesock_socket_real_sendall_continue_eagain_when_http(socket, old_socket):
    ("fakesock.socket#real_sendall should continue if the socket error was EAGAIN")
    socket.error = SocketErrorStub
    # Background: the real socket will stop returning bytes after the
    # first call
    real_socket = old_socket.return_value
    real_socket.recv.side_effect = [SocketErrorStub(errno.EAGAIN), b'after error', b""]

    # Given a fake socket
    socket = fakesock.socket()
    socket.is_http = True

    # When I call real_sendall with data, some args and kwargs
    socket.real_sendall(b"SOMEDATA", b'some extra args...', foo=b'bar')

    # Then it should have called sendall in the real socket
    real_socket.sendall.assert_called_once_with(b"SOMEDATA", b'some extra args...', foo=b'bar')

    # And the socket was set to blocking
    real_socket.setblocking.assert_called_once_with(1)

    # And recv was called with the bufsize
    real_socket.recv.assert_has_calls([
        call(socket._bufsize)
    ])

    # And the buffer should contain the data from the server
    socket.fd.read().should.equal(b"after error")

    # And connect was called
    real_socket.connect.called.should.be.true


@patch('httpretty.core.old_socket')
@patch('httpretty.core.socket')
def test_fakesock_socket_real_sendall_socket_error_when_http(socket, old_socket):
    ("fakesock.socket#real_sendall should continue if the socket error was EAGAIN")
    socket.error = SocketErrorStub
    # Background: the real socket will stop returning bytes after the
    # first call
    real_socket = old_socket.return_value
    real_socket.recv.side_effect = [SocketErrorStub(42), b'after error', ""]

    # Given a fake socket
    socket = fakesock.socket()
    socket.is_http = True

    # When I call real_sendall with data, some args and kwargs
    socket.real_sendall(b"SOMEDATA", b'some extra args...', foo=b'bar')

    # Then it should have called sendall in the real socket
    real_socket.sendall.assert_called_once_with(b"SOMEDATA", b'some extra args...', foo=b'bar')

    # And the socket was set to blocking
    real_socket.setblocking.assert_called_once_with(1)

    # And recv was called with the bufsize
    real_socket.recv.assert_called_once_with(socket._bufsize)

    # And the buffer should contain the data from the server
    socket.fd.read().should.equal(b"")

    # And connect was called
    real_socket.connect.called.should.be.true


@patch('httpretty.core.old_socket')
@patch('httpretty.core.POTENTIAL_HTTP_PORTS')
def test_fakesock_socket_real_sendall_when_sending_data(POTENTIAL_HTTP_PORTS, old_socket):
    ("fakesock.socket#real_sendall should connect before sending data")
    # Background: the real socket will stop returning bytes after the
    # first call
    real_socket = old_socket.return_value
    real_socket.recv.side_effect = [b'response from foobar :)', b""]

    # And the potential http port is 4000
    POTENTIAL_HTTP_PORTS.__contains__.side_effect = lambda other: int(other) == 4000
    POTENTIAL_HTTP_PORTS.union.side_effect = lambda other: POTENTIAL_HTTP_PORTS

    # Given a fake socket
    socket = fakesock.socket()

    # When I call connect to a server in a port that is considered HTTP
    socket.connect(('foobar.com', 4000))

    # And send some data
    socket.real_sendall(b"SOMEDATA")

    # Then connect should have been called
    real_socket.connect.assert_called_once_with(('foobar.com', 4000))

    # And the socket was set to blocking
    real_socket.setblocking.assert_called_once_with(1)

    # And recv was called with the bufsize
    real_socket.recv.assert_has_calls([
        call(socket._bufsize)
    ])

    # And the buffer should contain the data from the server
    socket.fd.read().should.equal(b"response from foobar :)")


@patch('httpretty.core.old_socket')
@patch('httpretty.core.httpretty')
@patch('httpretty.core.POTENTIAL_HTTP_PORTS')
def test_fakesock_socket_sendall_with_valid_requestline(POTENTIAL_HTTP_PORTS, httpretty, old_socket):
    ("fakesock.socket#sendall should create an entry if it's given a valid request line")
    matcher = Mock(name='matcher')
    info = Mock(name='info')
    httpretty.match_uriinfo.return_value = (matcher, info)
    httpretty.register_uri(httpretty.GET, 'http://foo.com/foobar')

    # Background:
    # using a subclass of socket that mocks out real_sendall
    class MySocket(fakesock.socket):
        def real_sendall(self, data, *args, **kw):
            raise AssertionError('should never call this...')

    # Given an instance of that socket
    socket = MySocket()

    # And that is is considered http
    socket.connect(('foo.com', 80))

    # When I try to send data
    socket.sendall(b"GET /foobar HTTP/1.1\r\nContent-Type: application/json\r\n\r\n")


@patch('httpretty.core.old_socket')
@patch('httpretty.core.httpretty')
@patch('httpretty.core.POTENTIAL_HTTP_PORTS')
def test_fakesock_socket_sendall_with_valid_requestline_2(POTENTIAL_HTTP_PORTS, httpretty, old_socket):
    ("fakesock.socket#sendall should create an entry if it's given a valid request line")
    matcher = Mock(name='matcher')
    info = Mock(name='info')
    httpretty.match_uriinfo.return_value = (matcher, info)
    httpretty.register_uri(httpretty.GET, 'http://foo.com/foobar')

    # Background:
    # using a subclass of socket that mocks out real_sendall
    class MySocket(fakesock.socket):
        def real_sendall(self, data, *args, **kw):
            raise AssertionError('should never call this...')

    # Given an instance of that socket
    socket = MySocket()

    # And that is is considered http
    socket.connect(('foo.com', 80))

    # When I try to send data
    socket.sendall(b"GET /foobar HTTP/1.1\r\nContent-Type: application/json\r\n\r\n")


@patch('httpretty.core.old_socket')
@patch('httpretty.core.POTENTIAL_HTTP_PORTS')
def test_fakesock_socket_sendall_with_body_data_no_entry(POTENTIAL_HTTP_PORTS, old_socket):
    ("fakesock.socket#sendall should call real_sendall when not parsing headers and there is no entry")
    # Background:
    # Using a subclass of socket that mocks out real_sendall

    class MySocket(fakesock.socket):
        def real_sendall(self, data):
            data.should.equal(b'BLABLABLABLA')
            return 'cool'

    # Given an instance of that socket
    socket = MySocket()
    socket._entry = None

    # And that is is considered http
    socket.connect(('foo.com', 80))

    # When I try to send data
    result = socket.sendall(b"BLABLABLABLA")

    # Then the result should be the return value from real_sendall
    result.should.equal('cool')


@patch('httpretty.core.old_socket')
@patch('httpretty.core.POTENTIAL_HTTP_PORTS')
def test_fakesock_socket_sendall_with_body_data_with_entry(POTENTIAL_HTTP_PORTS, old_socket):
    ("fakesock.socket#sendall should call real_sendall when there is no entry")
    # Background:
    # Using a subclass of socket that mocks out real_sendall
    data_sent = []

    class MySocket(fakesock.socket):
        def real_sendall(self, data):
            data_sent.append(data)

    # Given an instance of that socket
    socket = MySocket()

    # And that is is considered http
    socket.connect(('foo.com', 80))

    # When I try to send data
    socket.sendall(b"BLABLABLABLA")

    # Then it should have called real_sendall
    data_sent.should.equal([b'BLABLABLABLA'])


@patch('httpretty.core.httpretty.match_uriinfo')
@patch('httpretty.core.old_socket')
@patch('httpretty.core.POTENTIAL_HTTP_PORTS')
def test_fakesock_socket_sendall_with_body_data_with_chunked_entry(POTENTIAL_HTTP_PORTS, old_socket, match_uriinfo):
    ("fakesock.socket#sendall should call real_sendall when not ")
    # Background:
    # Using a subclass of socket that mocks out real_sendall

    class MySocket(fakesock.socket):
        def real_sendall(self, data):
            raise AssertionError('should have never been called')

    matcher = Mock(name='matcher')
    info = Mock(name='info')
    httpretty.match_uriinfo.return_value = (matcher, info)

    # Using a mocked entry
    entry = Mock()
    entry.method = 'GET'
    entry.info.path = '/foo'

    entry.request.headers = {
        'transfer-encoding': 'chunked',
    }
    entry.request.body = b''

    # Given an instance of that socket
    socket = MySocket()
    socket._entry = entry

    # And that is is considered http
    socket.connect(('foo.com', 80))

    # When I try to send data
    socket.sendall(b"BLABLABLABLA")

    # Then the entry should have that body
    httpretty.last_request.body.should.equal(b'BLABLABLABLA')
