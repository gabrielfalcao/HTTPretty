# #!/usr/bin/env python
# -*- coding: utf-8 -*-

# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2015>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals

import os
import json
import socket
import threading

import tornado.ioloop
import tornado.web
from functools import wraps

from os.path import abspath, dirname, join
from httpretty.core import POTENTIAL_HTTP_PORTS, old_socket


def get_free_tcp_port():
    """returns a TCP port that can be used for listen in the host.
    """
    tcp = old_socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    host, port = tcp.getsockname()
    tcp.close()
    return port


LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)
FIXTURE_FILE = lambda name: LOCAL_FILE('fixtures', name)


class JSONEchoHandler(tornado.web.RequestHandler):
    def get(self, matched):
        payload = dict([(x, self.get_argument(x)) for x in self.request.arguments])
        self.write(json.dumps({matched or 'index': payload}, indent=4))

    def post(self, matched):
        payload = dict(self.request.arguments)
        self.write(json.dumps({
            matched or 'index': payload,
            'req_body': self.request.body.decode('utf-8'),
            'req_headers': dict(self.request.headers.items()),
        }, indent=4))


class JSONEchoServer(threading.Thread):
    def __init__(self, lock, port, *args, **kw):
        self.lock = lock
        self.port = int(port)
        self._stop = threading.Event()
        super(JSONEchoServer, self).__init__(*args, **kw)
        self.daemon = True

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def setup_application(self):
        return tornado.web.Application([
            (r"/(.*)", JSONEchoHandler),
        ])

    def run(self):
        application = self.setup_application()
        application.listen(self.port)
        self.lock.release()
        tornado.ioloop.IOLoop.instance().start()


def use_tornado_server(callback):
    lock = threading.Lock()
    lock.acquire()

    @wraps(callback)
    def func(*args, **kw):
        port = os.getenv('TEST_PORT', get_free_tcp_port())
        POTENTIAL_HTTP_PORTS.add(port)
        kw['port'] = port
        server = JSONEchoServer(lock, port)
        server.start()
        try:
            lock.acquire()
            callback(*args, **kw)
        finally:
            lock.release()
            server.stop()
            if port in POTENTIAL_HTTP_PORTS:
                POTENTIAL_HTTP_PORTS.remove(port)
    return func
