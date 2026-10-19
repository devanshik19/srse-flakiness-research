import pytest
import socket
from django.core.servers.basehttp import WSGIServer

def test_wsgi_server_initialization():
    # Test with default parameters
    server_default = WSGIServer()
    assert server_default.address_family == socket.AF_INET
    assert server_default.allow_reuse_address is True

    # Test with ipv6 enabled
    server_ipv6 = WSGIServer(ipv6=True)
    assert server_ipv6.address_family == socket.AF_INET6
    assert server_ipv6.allow_reuse_address is True

    # Test with allow_reuse_address set to False
    server_no_reuse = WSGIServer(allow_reuse_address=False)
    assert server_no_reuse.address_family == socket.AF_INET
    assert server_no_reuse.allow_reuse_address is False