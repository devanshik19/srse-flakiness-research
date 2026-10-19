import pytest
import socket
from django.core.servers.basehttp import WSGIServer

def test_wsgi_server_init_ipv4():
    server = WSGIServer(request_queue_size=5)
    assert server.address_family == socket.AF_INET
    assert server.allow_reuse_address is True

def test_wsgi_server_init_ipv6():
    server = WSGIServer(request_queue_size=5, ipv6=True)
    assert server.address_family == socket.AF_INET6
    assert server.allow_reuse_address is True

def test_wsgi_server_init_allow_reuse_address_false():
    server = WSGIServer(request_queue_size=5, allow_reuse_address=False)
    assert server.allow_reuse_address is False