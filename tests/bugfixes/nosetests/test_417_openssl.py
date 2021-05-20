# This test is based on @ento's example snippet:
# https://gist.github.com/ento/e1e33d7d67e406bf03fe61f018404c21

# Original Issue:
# https://github.com/gabrielfalcao/HTTPretty/issues/417
import httpretty
import requests
import urllib3
from sure import expect
from unittest import skipIf
try:
    from urllib3.contrib.pyopenssl import extract_from_urllib3
except Exception:
    extract_from_urllib3 = None


@skipIf(extract_from_urllib3 is None,
        "urllib3.contrib.pyopenssl.extract_from_urllib3 does not exist")
def test_enable_disable_httpretty_extract():
    expect(urllib3.util.IS_PYOPENSSL).to.be.false
    httpretty.enable()
    httpretty.disable()
    extract_from_urllib3()
    expect(urllib3.util.IS_PYOPENSSL).to.be.false

def test_enable_disable_httpretty():
    expect(urllib3.util.IS_PYOPENSSL).to.be.false
    httpretty.enable()
    httpretty.disable()
    extract_from_urllib3()
    expect(urllib3.util.IS_PYOPENSSL).to.be.false
