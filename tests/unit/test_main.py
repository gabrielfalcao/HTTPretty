#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mock import patch
import httpretty
from httpretty.core import HTTPrettyRequest


@patch('httpretty.httpretty')
def test_last_request(original):
    ("httpretty.last_request() should return httpretty.core.last_request")

    httpretty.last_request().should.equal(original.last_request)


@patch('httpretty.httpretty')
def test_latest_requests(original):
    ("httpretty.latest_requests() should return httpretty.core.latest_requests")

    httpretty.latest_requests().should.equal(original.latest_requests)


def test_has_request():
    ("httpretty.has_request() correctly detects "
     "whether or not a request has been made")
    httpretty.reset()
    httpretty.has_request().should.be.false
    with patch('httpretty.httpretty.last_request', return_value=HTTPrettyRequest('')):
        httpretty.has_request().should.be.true
