import re
import json
import requests
from httpretty import httprettified, HTTPretty


@httprettified(verbose=True, allow_net_connect=False)
def test_basic_body():

   def my_callback(request, url, headers):
       body = {}
       import ipdb;ipdb.set_trace()
       return (200, headers, json.dumps(body))

   # Match any url via the regular expression
   HTTPretty.register_uri(HTTPretty.GET, re.compile(r'.*'), body=my_callback)
   HTTPretty.register_uri(HTTPretty.POST, re.compile(r'.*'), body=my_callback)

   # will trigger ipdb
   response = requests.post('https://test.com', data=json.dumps({'hello': 'world'}))
