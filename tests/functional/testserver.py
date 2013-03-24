# #!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# <HTTPretty - HTTP client mock for Python>
# Copyright (C) <2011-2013>  Gabriel Falcão <gabriel@nacaolivre.org>
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

try:
    import io
    StringIO = io.StringIO
except ImportError:
    import StringIO
    StringIO = StringIO.StringIO

import time
import socket
from tornado.web import Application
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from multiprocessing import Process

true_socket = socket.socket


class BubblesHandler(RequestHandler):
    def get(self):
        self.write(". o O 0 O o . o O 0 O o . o O 0 O o . o O 0 O o . o O 0 O o .")


class ComeHandler(RequestHandler):
    def get(self):
        self.write("<- HELLO WORLD ->")


class TornadoServer(object):
    is_running = False

    def __init__(self, port):
        self.port = int(port)
        self.process = None

    @classmethod
    def get_handlers(cls):
        return Application([
            (r"/go-for-bubbles/?", BubblesHandler),
            (r"/come-again/?", ComeHandler),
        ])

    def start(self):
        def go(app, port, data={}):
            from httpretty import HTTPretty
            HTTPretty.disable()
            http = HTTPServer(app)
            http.listen(int(port))
            IOLoop.instance().start()

        app = self.get_handlers()

        data = {}
        args = (app, self.port, data)
        self.process = Process(target=go, args=args)
        self.process.start()
        time.sleep(0.4)

    def stop(self):
        try:
            os.kill(self.process.pid, 9)
        except OSError:
            self.process.terminate()
        finally:
            self.is_running = False


class TCPServer(object):
    def __init__(self, port):
        self.port = int(port)

    def start(self):
        def go(port):
            from httpretty import HTTPretty
            HTTPretty.disable()
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', port))
            s.listen(True)
            conn, addr = s.accept()

            while True:
                data = conn.recv(1024)
                conn.send("RECEIVED: " + data)

            conn.close()

        args = [self.port]
        self.process = Process(target=go, args=args)
        self.process.start()
        time.sleep(0.4)

    def stop(self):
        try:
            os.kill(self.process.pid, 9)
        except OSError:
            self.process.terminate()
        finally:
            self.is_running = False


class TCPClient(object):
    def __init__(self, port):
        self.port = int(port)
        self.sock = true_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', self.port))

    def send(self, what):
        self.sock.sendall(str(what))
        return self.sock.recv(len(what) + 11)

    def close(self):
        try:
            self.sock.close()
        except socket.error:
            pass  # already closed

    def __del__(self):
        self.close()
