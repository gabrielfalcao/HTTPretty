#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mock import patch
import httpretty


@patch('httpretty.httpretty')
def test_last_request(original):
    """httpretty.last_request() should return httpretty.core.last_request"""
    httpretty.last_request().should.equal(original.last_request)
