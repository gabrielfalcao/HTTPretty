# File based on the snippet provided in https://github.com/gabrielfalcao/HTTPretty/issues/413#issue-787264551
import requests
import httpretty
import re


def mock_body(request, url, response_headers):
    return [200, response_headers, "Mocked " + url]


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_works_with_regex_path():
    "Issue #413 regex with path"
    patmatchpat = re.compile("/file-one")

    httpretty.register_uri(httpretty.GET, patmatchpat, body=mock_body)

    response = requests.get("https://example.com/file-one.html")
    response.status_code.should.equal(200)
    response.text.should.equal("Mocked https://example.com/file-one.html")

    response = requests.get("https://github.com/file-one.json")
    response.status_code.should.equal(200)
    response.text.should.equal("Mocked https://github.com/file-one.json")

@httpretty.activate(verbose=True, allow_net_connect=False)
def test_works_with_regex_dotall():
    "Issue #413 regex with .*"
    patmatchpat = re.compile(".*/file-two.*")

    httpretty.register_uri(httpretty.GET, patmatchpat, body=mock_body)

    response = requests.get("https://example.com/file-two.html")
    response.status_code.should.equal(200)
    response.text.should.equal("Mocked https://example.com/file-two.html")

    response = requests.get("https://github.com/file-two.json")
    response.status_code.should.equal(200)
    response.text.should.equal("Mocked https://github.com/file-two.json")
