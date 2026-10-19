import pytest
import socket
from django.core.servers.basehttp import WSGIServer

def test_wsgi_server_init_ipv4():
    server = WSGIServer(request_queue_size=5, allow_reuse_address=True)
    assert server.address_family == socket.AF_INET
    assert server.allow_reuse_address is True

def test_wsgi_server_init_ipv6():
    server = WSGIServer(request_queue_size=5, ipv6=True, allow_reuse_address=False)
    assert server.address_family == socket.AF_INET6
    assert server.allow_reuse_address is False

def test_wsgi_server_init_default():
    server = WSGIServer(request_queue_size=10)
    assert server.address_family == socket.AF_INET
    assert server.allow_reuse_address is True