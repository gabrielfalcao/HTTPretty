import httpretty
import httpx
from sure import expect

@httpretty.activate(verbose=True, allow_net_connect=False)
def test_httpx():
    "#414 httpx support"
    httpretty.register_uri(httpretty.GET, "https://blog.falcao.it/",
                           body="Posts")

    response = httpx.get('https://blog.falcao.it')

    expect(response.text).to.equal("Posts")
