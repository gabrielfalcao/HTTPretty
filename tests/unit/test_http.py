#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from httpretty.http import parse_requestline


def test_parse_request_line_connect():
    ("parse_requestline should parse the CONNECT method appropriately")

    # Given a valid request line string that has the CONNECT method
    line = "CONNECT / HTTP/1.1"

    # When I parse it
    result = parse_requestline(line)

    # Then it should return a tuple
    result.should.equal(("CONNECT", "/", "1.1"))
