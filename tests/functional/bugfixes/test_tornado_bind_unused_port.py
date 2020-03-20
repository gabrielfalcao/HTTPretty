import httpretty
from unittest import skip
from tornado.testing import bind_unused_port


@skip('')
@httpretty.activate(allow_net_connect=True)
def test_passthrough_binding_socket():
    # issue #247

    result = bind_unused_port()
    result.should.be.a(tuple)
    result.should.have.length_of(2)

    socket, port = result

    port.should.be.an(int)
    socket.close()
