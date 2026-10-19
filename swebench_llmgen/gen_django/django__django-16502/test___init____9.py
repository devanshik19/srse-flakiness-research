import pytest
import socket
from django.core.servers.basehttp import WSGIServer

def test_wsgi_server_init_ipv4():
    server = WSGIServer(allow_reuse_address=True)
    assert server.address_family == socket.AF_INET
    assert server.allow_reuse_address is True

def test_wsgi_server_init_ipv6():
    server = WSGIServer(ipv6=True, allow_reuse_address=False)
    assert server.address_family == socket.AF_INET6
    assert server.allow_reuse_address is False

def test_wsgi_server_init_default_params():
    server = WSGIServer()
    assert server.address_family == socket.AF_INET
    assert server.allow_reuse_address is True