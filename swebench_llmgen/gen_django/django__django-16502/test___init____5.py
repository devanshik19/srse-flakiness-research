import pytest
import socket
from django.core.servers.basehttp import WSGIServer

def test_wsgiserver_init_ipv6():
    server = WSGIServer(ipv6=True)
    assert server.address_family == socket.AF_INET6

def test_wsgiserver_init_ipv4():
    server = WSGIServer(ipv6=False)
    assert server.address_family == socket.AF_INET

def test_wsgiserver_init_allow_reuse_address():
    server = WSGIServer(allow_reuse_address=False)
    assert server.allow_reuse_address is False

def test_wsgiserver_init_default_allow_reuse_address():
    server = WSGIServer()
    assert server.allow_reuse_address is True