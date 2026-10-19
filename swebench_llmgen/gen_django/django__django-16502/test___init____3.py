import pytest
import socket
from django.core.servers.basehttp import WSGIServer

def test_wsgi_server_init():
    # Test default initialization
    server = WSGIServer()
    assert server.address_family == socket.AF_INET  # Default is IPv4
    assert server.allow_reuse_address is True
    
    # Test initialization with IPv6
    server_ipv6 = WSGIServer(ipv6=True)
    assert server_ipv6.address_family == socket.AF_INET6
    assert server_ipv6.allow_reuse_address is True
    
    # Test initialization with allow_reuse_address set to False
    server_no_reuse = WSGIServer(allow_reuse_address=False)
    assert server_no_reuse.address_family == socket.AF_INET  # Default is still IPv4
    assert server_no_reuse.allow_reuse_address is False